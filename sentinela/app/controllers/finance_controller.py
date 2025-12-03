from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.services.finance_service import FinanceService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from functools import wraps
from datetime import datetime

finance_bp = Blueprint('finance', __name__)
finance_service = FinanceService()
usuario_repository = UsuarioRepository()
fornecedor_repository = FornecedorRepository()

# Decorador para proteger rotas que requerem autenticação
def requer_autenticacao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'autenticado' not in session or not session.get('autenticado'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def obter_dados_usuario():
    """Busca todos os dados do usuário pela sessão"""
    if 'usuario_email' in session:
        usuario = usuario_repository.buscar_por_email(session['usuario_email'])
        if usuario:
            return {
                'nome': usuario.nome,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'endereco': usuario.endereco,
                'cpf': usuario.cpf
            }
    return {'nome': 'Usuário', 'email': '', 'telefone': '', 'endereco': '', 'cpf': ''}

@finance_bp.route('/dashboard')
@requer_autenticacao
def dashboard():
    resumo = finance_service.obter_resumo_dashboard()
    dados_usuario = obter_dados_usuario()
    return render_template('dashboard.html', resumo=resumo, usuario=dados_usuario)

@finance_bp.route('/boletos')
@requer_autenticacao
def boletos():
    lista_boletos = finance_service.listar_boletos()
    dados_usuario = obter_dados_usuario()
    return render_template('boletos.html', boletos=lista_boletos, usuario=dados_usuario)

@finance_bp.route('/notas-fiscais')
@requer_autenticacao
def notas_fiscais():
    lista_notas = finance_service.listar_notas_fiscais()
    dados_usuario = obter_dados_usuario()
    return render_template('notas_fiscais.html', notas=lista_notas, usuario=dados_usuario)


@finance_bp.route('/nota/<int:nota_id>/toggle-pago', methods=['POST'])
@requer_autenticacao
def toggle_pago_nota(nota_id):
    nota = finance_service.obter_nota_por_id(nota_id)
    if not nota:
        return redirect(url_for('finance.notas_fiscais'))

    novo_status = not nota.pago
    finance_service.atualizar_status_nota(nota_id, novo_status)
    return redirect(url_for('finance.notas_fiscais'))

@finance_bp.route('/perfil')
@requer_autenticacao
def perfil():
    dados_usuario = obter_dados_usuario()
    return render_template('perfil.html', usuario=dados_usuario)

@finance_bp.route('/fornecedores')
@requer_autenticacao
def fornecedores():
    lista_fornecedores = fornecedor_repository.listar_fornecedores()
    dados_usuario = obter_dados_usuario()
    return render_template('fornecedores.html', fornecedores=lista_fornecedores, usuario=dados_usuario)

@finance_bp.route('/fornecedor/<int:fornecedor_id>')
@requer_autenticacao
def detalhes_fornecedor(fornecedor_id):
    fornecedor = fornecedor_repository.buscar_por_id(fornecedor_id)
    dados_usuario = obter_dados_usuario()
    if not fornecedor:
        return redirect(url_for('finance.fornecedores'))
    return render_template('detalhes_fornecedor.html', fornecedor=fornecedor, usuario=dados_usuario)

@finance_bp.route('/adicionar-boleto', methods=['GET', 'POST'])
@requer_autenticacao
def adicionar_boleto():
    dados_usuario = obter_dados_usuario()
    fornecedores = finance_service.listar_fornecedores()
    
    if request.method == 'POST':
        try:
            # Validação de campos obrigatórios
            codigo = request.form.get('codigo', '').strip()
            vencimento_str = request.form.get('vencimento', '').strip()
            valor_str = request.form.get('valor', '').strip()
            status = request.form.get('status', 'A vencer').strip()
            tipo = request.form.get('tipo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            fornecedor_id_str = request.form.get('fornecedor_id', '').strip()
            
            # Validações
            erros = []
            if not codigo:
                erros.append("Código de barras é obrigatório")
            if not vencimento_str:
                erros.append("Data de vencimento é obrigatória")
            if not valor_str:
                erros.append("Valor é obrigatório")
            
            if erros:
                return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro=" | ".join(erros))
            
            try:
                valor = float(valor_str)
                if valor <= 0:
                    return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Valor deve ser maior que zero")
            except ValueError:
                return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Valor inválido")
            
            try:
                vencimento = datetime.strptime(vencimento_str, '%Y-%m-%d').date()
            except ValueError:
                return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Data de vencimento inválida")
            
            fornecedor_id = None
            if fornecedor_id_str:
                try:
                    fornecedor_id = int(fornecedor_id_str)
                except ValueError:
                    pass
            
            finance_service.criar_boleto(
                status=status,
                codigo=codigo,
                vencimento=vencimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                fornecedor_id=fornecedor_id
            )
            return redirect(url_for('finance.boletos'))
        except Exception as e:
            return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro=f"Erro ao salvar: {str(e)}")
    
    return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario)

@finance_bp.route('/adicionar-nota-fiscal', methods=['GET', 'POST'])
@requer_autenticacao
def adicionar_nota_fiscal():
    dados_usuario = obter_dados_usuario()
    fornecedores = finance_service.listar_fornecedores()
    
    if request.method == 'POST':
        try:
            # Validação de campos obrigatórios
            codigo = request.form.get('codigo', '').strip()
            recebimento_str = request.form.get('recebimento', '').strip()
            valor_str = request.form.get('valor', '').strip()
            tipo = request.form.get('tipo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            pago = request.form.get('pago') == 'on'
            fornecedor_id_str = request.form.get('fornecedor_id', '').strip()
            
            # Validações
            erros = []
            if not codigo:
                erros.append("Número da nota é obrigatório")
            if not recebimento_str:
                erros.append("Data de recebimento é obrigatória")
            if not valor_str:
                erros.append("Valor é obrigatório")
            
            if erros:
                return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro=" | ".join(erros))
            
            try:
                valor = float(valor_str)
                if valor <= 0:
                    return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Valor deve ser maior que zero")
            except ValueError:
                return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Valor inválido")
            
            try:
                recebimento = datetime.strptime(recebimento_str, '%Y-%m-%d').date()
            except ValueError:
                return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro="Data de recebimento inválida")
            
            fornecedor_id = None
            if fornecedor_id_str:
                try:
                    fornecedor_id = int(fornecedor_id_str)
                except ValueError:
                    pass
            
            finance_service.criar_nota_fiscal(
                codigo=codigo,
                recebimento=recebimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                fornecedor_id=fornecedor_id,
                pago=pago
            )
            return redirect(url_for('finance.notas_fiscais'))
        except Exception as e:
            return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro=f"Erro ao salvar: {str(e)}")
    
    return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario)

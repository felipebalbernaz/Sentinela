from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.services.finance_service import FinanceService
from app.repositories.fornecedor_repository import FornecedorRepository
from app.services.ocr_service import OCRService
from datetime import datetime
import os
from werkzeug.utils import secure_filename

finance_bp = Blueprint('finance', __name__)
finance_service = FinanceService()
fornecedor_repository = FornecedorRepository()
ocr_service = OCRService()

# Configurações de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def obter_dados_usuario():
    """Busca todos os dados do usuário logado"""
    if current_user.is_authenticated:
        return {
            'nome': current_user.nome,
            'email': current_user.email,
            'telefone': current_user.telefone,
            'endereco': current_user.endereco,
            'cpf': current_user.cpf
        }
    return {'nome': 'Usuário', 'email': '', 'telefone': '', 'endereco': '', 'cpf': ''}

@finance_bp.route('/dashboard')
@login_required
def dashboard():
    resumo = finance_service.obter_resumo_dashboard(current_user.id)
    dados_usuario = obter_dados_usuario()
    return render_template('dashboard.html', resumo=resumo, usuario=dados_usuario)

@finance_bp.route('/boletos')
@login_required
def boletos():
    lista_boletos = finance_service.listar_boletos(current_user.id)
    dados_usuario = obter_dados_usuario()
    return render_template('boletos.html', boletos=lista_boletos, usuario=dados_usuario)

@finance_bp.route('/notas-fiscais')
@login_required
def notas_fiscais():
    lista_notas = finance_service.listar_notas_fiscais(current_user.id)
    dados_usuario = obter_dados_usuario()
    return render_template('notas_fiscais.html', notas=lista_notas, usuario=dados_usuario)


@finance_bp.route('/nota/<int:nota_id>/toggle-pago', methods=['POST'])
@login_required
def toggle_pago_nota(nota_id):
    nota = finance_service.obter_nota_por_id(nota_id, current_user.id)
    if not nota:
        flash('Nota fiscal não encontrada ou você não tem permissão para acessá-la.', 'error')
        return redirect(url_for('finance.notas_fiscais'))

    novo_status = not nota.pago
    finance_service.atualizar_status_nota(nota_id, novo_status, current_user.id)
    flash('Status da nota fiscal atualizado com sucesso!', 'success')
    return redirect(url_for('finance.notas_fiscais'))

@finance_bp.route('/perfil')
@login_required
def perfil():
    dados_usuario = obter_dados_usuario()
    return render_template('perfil.html', usuario=dados_usuario)

@finance_bp.route('/fornecedores')
@login_required
def fornecedores():
    lista_fornecedores = fornecedor_repository.listar_fornecedores()
    dados_usuario = obter_dados_usuario()
    return render_template('fornecedores.html', fornecedores=lista_fornecedores, usuario=dados_usuario)

@finance_bp.route('/fornecedor/<int:fornecedor_id>')
@login_required
def detalhes_fornecedor(fornecedor_id):
    fornecedor = fornecedor_repository.buscar_por_id(fornecedor_id)
    dados_usuario = obter_dados_usuario()
    if not fornecedor:
        flash('Fornecedor não encontrado.', 'error')
        return redirect(url_for('finance.fornecedores'))
    return render_template('detalhes_fornecedor.html', fornecedor=fornecedor, usuario=dados_usuario)

@finance_bp.route('/processar-ocr-boleto', methods=['POST'])
@login_required
def processar_ocr_boleto():
    """Endpoint para processar OCR de boleto via AJAX"""
    try:
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Nenhuma imagem enviada'}), 400
        
        file = request.files['imagem']
        if file.filename == '':
            return jsonify({'erro': 'Nenhuma imagem selecionada'}), 400
        
        if file and allowed_file(file.filename):
            image_bytes = file.read()
            dados_extraidos = ocr_service.extract_boleto_data(image_bytes)
            return jsonify({'sucesso': True, 'dados': dados_extraidos})
        else:
            return jsonify({'erro': 'Formato de arquivo não permitido'}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar OCR: {str(e)}'}), 500

@finance_bp.route('/processar-ocr-nota', methods=['POST'])
@login_required
def processar_ocr_nota():
    """Endpoint para processar OCR de nota fiscal via AJAX"""
    try:
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Nenhuma imagem enviada'}), 400
        
        file = request.files['imagem']
        if file.filename == '':
            return jsonify({'erro': 'Nenhuma imagem selecionada'}), 400
        
        if file and allowed_file(file.filename):
            image_bytes = file.read()
            dados_extraidos = ocr_service.extract_nota_fiscal_data(image_bytes)
            return jsonify({'sucesso': True, 'dados': dados_extraidos})
        else:
            return jsonify({'erro': 'Formato de arquivo não permitido'}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar OCR: {str(e)}'}), 500

@finance_bp.route('/adicionar-boleto', methods=['GET', 'POST'])
@login_required
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
                usuario_id=current_user.id,
                fornecedor_id=fornecedor_id
            )
            flash('Boleto adicionado com sucesso!', 'success')
            return redirect(url_for('finance.boletos'))
        except Exception as e:
            return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario, erro=f"Erro ao salvar: {str(e)}")
    
    return render_template('adicionar_boleto.html', fornecedores=fornecedores, usuario=dados_usuario)

@finance_bp.route('/adicionar-nota-fiscal', methods=['GET', 'POST'])
@login_required
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
                usuario_id=current_user.id,
                fornecedor_id=fornecedor_id,
                pago=pago
            )
            flash('Nota fiscal adicionada com sucesso!', 'success')
            return redirect(url_for('finance.notas_fiscais'))
        except Exception as e:
            return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario, erro=f"Erro ao salvar: {str(e)}")
    
    return render_template('adicionar_nota_fiscal.html', fornecedores=fornecedores, usuario=dados_usuario)

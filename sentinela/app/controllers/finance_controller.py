from flask import Blueprint, render_template, redirect, url_for, session
from app.services.finance_service import FinanceService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from functools import wraps

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

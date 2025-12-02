from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.auth_service import AuthService

main_bp = Blueprint('main', __name__)
auth_service = AuthService()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')
        success, message = auth_service.login(email, senha)
        if success:
            # Armazena o usuário na sessão
            session['usuario_email'] = email
            session['autenticado'] = True
            return redirect(url_for('finance.dashboard'))
        else:
            # Retorna a página de login com mensagem de erro
            return render_template('index.html', error_message=message)
    return render_template('index.html')

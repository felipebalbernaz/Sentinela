from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.services.auth_service import AuthService

main_bp = Blueprint('main', __name__)
auth_service = AuthService()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')
        success, usuario, message = auth_service.login(email, senha)
        if success and usuario:
            # Usa Flask-Login para fazer login
            login_user(usuario, remember=True)
            flash(message, 'success')
            return redirect(url_for('finance.dashboard'))
        else:
            # Retorna a página de login com mensagem de erro
            return render_template('index.html', error_message=message)
    return render_template('index.html')

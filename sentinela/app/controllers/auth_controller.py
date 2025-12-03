from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import AuthService

# criando blueprints de registro e login
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            return render_template('index.html', error_message=message)
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from form
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('password')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        cpf = request.form.get('cpf')
        
        # Tentar registrar o usuário
        success, resultado = auth_service.registrar_usuario(nome, email, senha, telefone, endereco, cpf)
        if success:
            # Login automático após registro
            login_user(resultado, remember=True)
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('finance.dashboard'))
        else:
            return render_template('register.html', error_message=resultado)
            
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso.', 'info')
    return redirect(url_for('main.index'))

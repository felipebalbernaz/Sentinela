from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService

# criando blueprints de registro e login
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            # flash(message) # Flash messages require secret key setup in template
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
        success, message = auth_service.registrar_usuario(nome, email, senha, telefone, endereco, cpf)
        if success:
            return redirect(url_for('main.index'))
        else:
            return render_template('register.html', error_message=message)
            
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

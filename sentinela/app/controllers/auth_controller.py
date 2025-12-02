from flask import Blueprint, render_template, request, redirect, url_for, flash
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
            return redirect(url_for('finance.dashboard'))
        else:
            # flash(message) # Flash messages require secret key setup in template
            pass
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from form
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('password')
        # ... other fields ...
        
        # For simplicity, passing minimal data
        success, message = auth_service.registrar_usuario(nome, email, senha, None, None, None)
        if success:
            return redirect(url_for('auth.login'))
            
    return render_template('register.html')

from flask import Blueprint, render_template
# criando blueprints de registro e login
auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login')
def login():
    return render_template('index.html')
@auth_bp.route('/register')
def register():
    return render_template('register.html')

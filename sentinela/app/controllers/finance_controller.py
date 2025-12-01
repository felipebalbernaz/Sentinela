from flask import Blueprint, render_template

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@finance_bp.route('/boletos')
def boletos():
    return render_template('boletos.html')

@finance_bp.route('/notas-fiscais')
def notas_fiscais():
    return render_template('notas_fiscais.html')

from flask import Blueprint, render_template
from app.services.finance_service import FinanceService

finance_bp = Blueprint('finance', __name__)
finance_service = FinanceService()

@finance_bp.route('/dashboard')
def dashboard():
    resumo = finance_service.obter_resumo_dashboard()
    return render_template('dashboard.html', resumo=resumo)

@finance_bp.route('/boletos')
def boletos():
    lista_boletos = finance_service.listar_boletos()
    return render_template('boletos.html', boletos=lista_boletos)

@finance_bp.route('/notas-fiscais')
def notas_fiscais():
    lista_notas = finance_service.listar_notas_fiscais()
    return render_template('notas_fiscais.html', notas=lista_notas)

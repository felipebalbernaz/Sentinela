from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicializa o objeto SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a app
    db.init_app(app)

    # Importa os models para que o SQLAlchemy os reconheça
    # Importação dentro da função ou após a criação de db para evitar importação circular
    from app.models.usuario import Usuario
    from app.models.fornecedor import Fornecedor
    from app.models.boleto import Boleto
    from app.models.nota_fiscal import NotaFiscal

    # Registra os Blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.finance_controller import finance_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(finance_bp)

    # Cria as tabelas do banco de dados (apenas para desenvolvimento)
    with app.app_context():
        db.create_all()

    return app

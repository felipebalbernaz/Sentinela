from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicializa o objeto SQLAlchemy
db = SQLAlchemy()

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Callback para carregar o usuário a partir do ID armazenado na sessão"""
    from app.models.usuario import Usuario
    return Usuario.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a app
    db.init_app(app)
    login_manager.init_app(app)

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

    # Cria as tabelas do banco de dados
    # Se o banco existir com estrutura antiga, será recriado automaticamente
    with app.app_context():
        try:
            # Tenta verificar se a estrutura está correta
            from app.models.usuario import Usuario
            # Tenta fazer uma query simples para verificar se a estrutura está OK
            # Se a coluna senha_hash não existir, dará erro e recriaremos o banco
            Usuario.query.limit(1).all()
            # Se chegou aqui, a estrutura está OK - apenas garante que todas as tabelas existem
            db.create_all()
        except Exception:
            # Se houver erro (estrutura antiga, coluna não existe, ou banco não existe)
            # Recria o banco do zero
            try:
                db.drop_all()
            except:
                pass
            db.create_all()

    return app

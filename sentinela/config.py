import os
from pathlib import Path

# Caminho base do projeto
basedir = Path(__file__).resolve().parent
# Caminho para a pasta instance (onde o banco será criado)
instance_path = basedir / 'instance'

# Criar pasta instance se não existir
instance_path.mkdir(exist_ok=True)

class Config:
    # Chave secreta para sessões e segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'
    # URI do banco de dados (SQLite por padrão)
    # Usa caminho absoluto para evitar problemas
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{instance_path / "sentinela.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de upload
    UPLOAD_FOLDER = basedir / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Criar pasta de uploads se não existir
    UPLOAD_FOLDER.mkdir(exist_ok=True)
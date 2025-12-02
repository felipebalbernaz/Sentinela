import os

class Config:
    # Chave secreta para sessões e segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'
    # URI do banco de dados (SQLite por padrão)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sentinela.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from app import db
from app.models.usuario import Usuario

class UsuarioRepository:
    def salvar(self, usuario: Usuario):
        try:
            db.session.add(usuario)
            db.session.commit()
            print(f"Usuário {usuario.nome} salvo no banco de dados.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar usuário: {e}")
            raise e

    def buscar_por_email(self, email: str):
        return Usuario.query.filter_by(email=email).first()

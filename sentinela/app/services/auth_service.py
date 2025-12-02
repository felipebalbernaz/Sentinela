from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

class AuthService:
    def __init__(self):
        self.usuario_repository = UsuarioRepository()

    def registrar_usuario(self, nome, email, senha, telefone, endereco, cpf):
        # Lógica de negócio: Verificar se o usuário já existe
        if self.usuario_repository.buscar_por_email(email):
            return False, "Usuário já existe."
        
        novo_usuario = Usuario(nome, email, senha, telefone, endereco, cpf)
        self.usuario_repository.salvar(novo_usuario)
        return True, "Usuário registrado com sucesso."

    def login(self, email, senha):
        usuario = self.usuario_repository.buscar_por_email(email)
        if usuario and usuario.senha == senha:
            return True, "Login realizado com sucesso."
        return False, "Credenciais inválidas."

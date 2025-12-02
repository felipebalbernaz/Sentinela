from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

class AuthService:
    def __init__(self):
        self.usuario_repository = UsuarioRepository()

    def registrar_usuario(self, nome, email, senha, telefone, endereco, cpf):
        # Validar campos obrigatórios
        if not nome or not email or not senha:
            return False, "Nome, email e senha são obrigatórios."
        
        # Validar formato de email básico
        if '@' not in email or '.' not in email:
            return False, "Email inválido."
        
        # Verificar se o usuário já existe
        if self.usuario_repository.buscar_por_email(email):
            return False, "Usuário já existe."
        
        # Validar comprimento mínimo de senha
        if len(senha) < 4:
            return False, "Senha deve ter no mínimo 4 caracteres."
        
        novo_usuario = Usuario(nome, email, senha, telefone, endereco, cpf)
        self.usuario_repository.salvar(novo_usuario)
        return True, "Usuário registrado com sucesso."

    def login(self, email, senha):
        # Validar se email e senha não estão vazios
        if not email or not senha:
            return False, "Email e senha são obrigatórios."
        
        usuario = self.usuario_repository.buscar_por_email(email)
        
        # Verificar se usuário existe
        if not usuario:
            return False, "Usuário não encontrado."
        
        # Verificar se senha está correta
        if usuario.senha != senha:
            return False, "Senha incorreta."
        
        return True, "Login realizado com sucesso."

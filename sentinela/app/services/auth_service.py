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
        
        # Criar usuário (a senha será hasheada automaticamente no __init__)
        novo_usuario = Usuario(nome, email, senha, telefone, endereco, cpf)
        self.usuario_repository.salvar(novo_usuario)
        return True, novo_usuario  # Retorna o objeto usuário para login automático

    def login(self, email, senha):
        # Validar se email e senha não estão vazios
        if not email or not senha:
            return False, None, "Email e senha são obrigatórios."
        
        usuario = self.usuario_repository.buscar_por_email(email)
        
        # Verificar se usuário existe
        if not usuario:
            return False, None, "Usuário não encontrado."
        
        # Verificar se senha está correta usando check_senha (compara hash)
        if not usuario.check_senha(senha):
            return False, None, "Senha incorreta."
        
        return True, usuario, "Login realizado com sucesso."

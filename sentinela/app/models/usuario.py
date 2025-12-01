class Usuario:
    def __init__(self, nome, email, senha, telefone, endereco, cpf):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__telefone = telefone
        self.__endereco = endereco
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

    @property
    def cpf(self):
        return self.__cpf

    def excluirConta(self):
        self.nome = None
        self.email = None
        self.senha = None
        self.telefone = None
        self.endereco = None
        self.cpf = None
        print("Conta excluída com sucesso!")

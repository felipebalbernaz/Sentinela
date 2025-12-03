# 🛡️ Sentinela - Sistema de Gestão Financeira

Sistema web para gestão de boletos e notas fiscais, desenvolvido em Python com Flask.

## 📋 Características

- ✅ Autenticação de usuários com Flask-Login
- ✅ Gestão de boletos (cadastro, listagem, controle de vencimento)
- ✅ Gestão de notas fiscais (cadastro, listagem, marcação de pagamento)
- ✅ Cadastro de fornecedores
- ✅ Dashboard com resumo financeiro
- ✅ Isolamento de dados por usuário
- ✅ Senhas protegidas com hash (Werkzeug)

## 🏗️ Arquitetura

O projeto segue uma **arquitetura em camadas** (Layered Architecture):

```
Controllers → Services → Repositories → Models
```

- **Controllers**: Rotas HTTP e endpoints
- **Services**: Lógica de negócio
- **Repositories**: Acesso ao banco de dados
- **Models**: Entidades do domínio (SQLAlchemy ORM)

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd sentinela
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   python run.py
   ```

4. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

### Popular com Dados de Teste (Opcional)

Para popular o banco de dados com dados de exemplo:

```bash
python instance/seed_db.py
```

**Credenciais de teste:**
- Email: `teste@email.com`
- Senha: `senha123`

## 📁 Estrutura do Projeto

```
sentinela/
├── app/
│   ├── controllers/      # Rotas HTTP (Blueprints)
│   ├── services/         # Lógica de negócio
│   ├── repositories/     # Acesso ao banco de dados
│   ├── models/           # Modelos SQLAlchemy
│   └── templates/        # Templates HTML (Flask)
├── instance/             # Banco de dados SQLite
├── config.py             # Configurações
├── run.py               # Ponto de entrada
└── requirements.txt      # Dependências
```

## 🗄️ Banco de Dados

O projeto usa **SQLite** como banco de dados. O arquivo `instance/sentinela.db` é criado automaticamente na primeira execução.

### Estrutura das Tabelas

- **usuarios**: Dados dos usuários do sistema
- **fornecedores**: Cadastro de fornecedores
- **boletos**: Boletos cadastrados (vinculados a usuários)
- **notas_fiscais**: Notas fiscais cadastradas (vinculadas a usuários)

## 🔐 Segurança

- Senhas são armazenadas como **hash** (não texto puro)
- Autenticação gerenciada por **Flask-Login**
- Cada usuário só acessa seus próprios dados
- Validação de permissões antes de operações

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-Login**: Gerenciamento de autenticação
- **Werkzeug**: Hash de senhas
- **SQLite**: Banco de dados

## 📝 Notas Importantes

1. **Primeira Execução**: O banco de dados será criado automaticamente. Se você tiver um banco antigo com estrutura diferente, ele será recriado automaticamente.

2. **Desenvolvimento**: O projeto está configurado para modo de desenvolvimento (`debug=True`). Para produção, ajuste as configurações em `config.py`.

3. **Banco de Dados**: O arquivo `instance/sentinela.db` é criado automaticamente. Este arquivo está no `.gitignore` e não deve ser commitado.

## 🐛 Solução de Problemas

### Erro: "no such column: usuarios.senha_hash"

Se você encontrar este erro, significa que há um banco de dados antigo. A aplicação tentará recriar automaticamente. Se o problema persistir:

1. Delete o arquivo `instance/sentinela.db`
2. Execute a aplicação novamente
3. O banco será criado com a estrutura correta

### Erro ao fazer login

- Verifique se o usuário existe no banco de dados
- Execute o script de seed para criar usuário de teste: `python instance/seed_db.py`

## 📄 Licença

Este projeto foi desenvolvido como trabalho acadêmico de POO (Programação Orientada a Objetos).

## 👥 Contribuição

Este é um projeto acadêmico. Para sugestões ou melhorias, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Flask e Python**


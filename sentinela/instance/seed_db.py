"""
Script para popular o banco de dados com dados de teste
Execute este script uma única vez antes de usar a aplicação
"""

from app import create_app, db
from app.models.usuario import Usuario
from app.models.fornecedor import Fornecedor
from app.models.boleto import Boleto
from app.models.nota_fiscal import NotaFiscal
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Limpar dados anteriores (descomente para resetar)
    # db.drop_all()
    # db.create_all()

    # Verificar se já existe usuário de teste
    usuario_existente = Usuario.query.filter_by(email='teste@email.com').first()
    
    if not usuario_existente:
        print("Criando usuário de teste...")
        usuario = Usuario(
            nome='Usuário Teste',
            email='teste@email.com',
            senha='senha123',
            telefone='11999999999',
            endereco='Rua Teste, 123',
            cpf='12345678901'
        )
        db.session.add(usuario)
        db.session.commit()
        print(f"✓ Usuário criado: teste@email.com / senha123")
    else:
        print("✓ Usuário de teste já existe")

    # Criar fornecedor de teste
    fornecedor_existente = Fornecedor.query.filter_by(cnpj='12345678901234').first()
    
    if not fornecedor_existente:
        print("Criando fornecedores de teste...")
        fornecedor1 = Fornecedor(
            nome='Fornecedor Teste LTDA',
            cnpj='12345678901234',
            endereco='Av. Principal, 456',
            contato='contato@fornecedor.com'
        )
        fornecedor2 = Fornecedor(
            nome='Distribuidora ABC',
            cnpj='98765432109876',
            endereco='Rua Secundária, 789',
            contato='vendas@distribuidora.com'
        )
        fornecedor3 = Fornecedor(
            nome='Serviços Gerais XYZ',
            cnpj='11122233344455',
            endereco='Av. Comercial, 1000',
            contato='atendimento@servicos.com'
        )
        db.session.add(fornecedor1)
        db.session.add(fornecedor2)
        db.session.add(fornecedor3)
        db.session.commit()
        print(f"✓ {3} fornecedores criados")
    else:
        print("✓ Fornecedores de teste já existem")

    # Criar boletos de teste
    boletos_existentes = Boleto.query.count()
    
    if boletos_existentes == 0:
        print("Criando boletos de teste...")
        # Buscar usuário e fornecedores criados
        usuario_teste = Usuario.query.filter_by(email='teste@email.com').first()
        if not usuario_teste:
            print("⚠ Erro: Usuário de teste não encontrado. Crie o usuário primeiro.")
        else:
            forn1 = Fornecedor.query.filter_by(cnpj='12345678901234').first()
            forn2 = Fornecedor.query.filter_by(cnpj='98765432109876').first()
            
            boleto1 = Boleto(
                status='A vencer',
                codigo='12345.67890 12345.678901 12345.678901 1 12345678901234',
                vencimento=datetime.now().date() + timedelta(days=10),
                valor=1500.00,
                tipo='Pagamento',
                descricao='Pagamento de materiais',
                usuario_id=usuario_teste.id,
                fornecedor_id=forn1.id if forn1 else None
            )
            boleto2 = Boleto(
                status='Vencido',
                codigo='98765.43210 98765.432101 98765.432101 1 98765432101234',
                vencimento=datetime.now().date() - timedelta(days=5),
                valor=2500.00,
                tipo='Pagamento',
                descricao='Pagamento de serviços',
                usuario_id=usuario_teste.id,
                fornecedor_id=forn2.id if forn2 else None
            )
            db.session.add(boleto1)
            db.session.add(boleto2)
            db.session.commit()
            print(f"✓ {2} boletos criados")
    else:
        print(f"✓ Boletos já existem ({boletos_existentes})")

    # Criar notas fiscais de teste
    notas_existentes = NotaFiscal.query.count()
    
    if notas_existentes == 0:
        print("Criando notas fiscais de teste...")
        # Buscar usuário e fornecedores criados
        usuario_teste = Usuario.query.filter_by(email='teste@email.com').first()
        if not usuario_teste:
            print("⚠ Erro: Usuário de teste não encontrado. Crie o usuário primeiro.")
        else:
            forn1 = Fornecedor.query.filter_by(cnpj='12345678901234').first()
            forn3 = Fornecedor.query.filter_by(cnpj='11122233344455').first()
            
            nota1 = NotaFiscal(
                codigo='NF-001',
                recebimento=datetime.now().date(),
                valor=5000.00,
                tipo='Entrada',
                descricao='Nota fiscal de entrada',
                usuario_id=usuario_teste.id,
                pago=False,
                fornecedor_id=forn1.id if forn1 else None
            )
            nota2 = NotaFiscal(
                codigo='NF-002',
                recebimento=datetime.now().date() - timedelta(days=2),
                valor=3000.00,
                tipo='Entrada',
                descricao='Nota fiscal de entrada',
                usuario_id=usuario_teste.id,
                pago=False,
                fornecedor_id=forn3.id if forn3 else None
            )
            db.session.add(nota1)
            db.session.add(nota2)
            db.session.commit()
            print(f"✓ {2} notas fiscais criadas")
    else:
        print(f"✓ Notas fiscais já existem ({notas_existentes})")

    print("\n✓ Banco de dados populado com sucesso!")
    print("\nCredenciais de teste:")
    print("Email: teste@email.com")
    print("Senha: senha123")

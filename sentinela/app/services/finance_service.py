from app.repositories.finance_repository import FinanceRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from app.models.boleto import Boleto
from app.models.nota_fiscal import NotaFiscal
from datetime import datetime

class FinanceService:
    def __init__(self):
        self.finance_repository = FinanceRepository()
        self.fornecedor_repository = FornecedorRepository()

    def obter_resumo_dashboard(self):
        # Lógica de negócio para calcular totais
        boletos = self.finance_repository.listar_boletos()
        
        # Calcular somas e contagens por status
        a_vencer = {'valor': 0.0, 'quantidade': 0}
        vencidos = {'valor': 0.0, 'quantidade': 0}
        pagos = {'valor': 0.0, 'quantidade': 0}
        
        for boleto in boletos:
            if boleto.status == 'A vencer':
                a_vencer['valor'] += boleto.valor
                a_vencer['quantidade'] += 1
            elif boleto.status == 'Vencido':
                vencidos['valor'] += boleto.valor
                vencidos['quantidade'] += 1
            elif boleto.status == 'Pago':
                pagos['valor'] += boleto.valor
                pagos['quantidade'] += 1
        
        return {
            "a_vencer": a_vencer,
            "vencidos": vencidos,
            "pagos": pagos
        }

    def obter_ultimos_documentos(self, limite=3):
        """Retorna os últimos 3 documentos (boletos e notas fiscais) ordenados por data de criação"""
        boletos = self.finance_repository.listar_boletos()
        notas = self.finance_repository.listar_notas_fiscais()
        
        documentos = []
        
        # Adicionar boletos
        for boleto in boletos:
            documentos.append({
                'tipo': 'Boleto',
                'id': boleto.id,
                'descricao': boleto.descricao,
                'codigo': boleto.codigo,
                'data': boleto.vencimento,
                'valor': boleto.valor,
                'status': boleto.status,
                'fornecedor': boleto.fornecedor.nome if boleto.fornecedor else '-'
            })
        
        # Adicionar notas fiscais
        for nota in notas:
            documentos.append({
                'tipo': 'Nota Fiscal',
                'id': nota.id,
                'descricao': nota.descricao,
                'codigo': nota.codigo,
                'data': nota.recebimento,
                'valor': nota.valor,
                'status': 'Pago' if nota.pago else 'Não Pago',
                'fornecedor': nota.fornecedor.nome if nota.fornecedor else '-'
            })
        
        # Ordenar por data descrescente e pegar apenas os últimos 'limite'
        documentos.sort(key=lambda x: x['data'], reverse=True)
        return documentos[:limite]

    def listar_boletos(self, search_query=None, status_filter=None):
        return self.finance_repository.listar_boletos(search_query, status_filter)

    def listar_notas_fiscais(self, search_query=None, status_filter=None):
        return self.finance_repository.listar_notas_fiscais(search_query, status_filter)

    def obter_nota_por_id(self, nota_id: int):
        return self.finance_repository.buscar_nota_por_id(nota_id)

    def atualizar_status_nota(self, nota_id: int, pago: bool):
        return self.finance_repository.atualizar_status_nota(nota_id, pago)

    def listar_fornecedores(self):
        return self.fornecedor_repository.listar_fornecedores()

    def obter_boleto_por_id(self, boleto_id: int):
        return self.finance_repository.buscar_boleto_por_id(boleto_id)

    def atualizar_status_boleto(self, boleto_id: int, status: str):
        return self.finance_repository.atualizar_status_boleto(boleto_id, status)

    def criar_boleto(self, status, codigo, vencimento, valor, tipo, descricao, fornecedor_id=None):
        try:
            boleto = Boleto(
                status=status,
                codigo=codigo,
                vencimento=vencimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                fornecedor_id=fornecedor_id
            )
            self.finance_repository.salvar_boleto(boleto)
            return boleto
        except Exception as e:
            print(f"Erro ao criar boleto: {e}")
            raise e

    def criar_nota_fiscal(self, codigo, recebimento, valor, tipo, descricao, fornecedor_id=None, pago=False):
        try:
            nota = NotaFiscal(
                codigo=codigo,
                recebimento=recebimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                fornecedor_id=fornecedor_id,
                pago=pago
            )
            self.finance_repository.salvar_nota_fiscal(nota)
            return nota
        except Exception as e:
            print(f"Erro ao criar nota fiscal: {e}")
            raise e

    def deletar_nota_fiscal(self, nota_id: int):
        return self.finance_repository.deletar_nota_fiscal(nota_id)

    def atualizar_nota_fiscal(self, nota_id, codigo, recebimento, valor, tipo, descricao, fornecedor_id, pago):
        return self.finance_repository.atualizar_nota_fiscal(
            nota_id=nota_id,
            codigo=codigo,
            recebimento=recebimento,
            valor=valor,
            tipo=tipo,
            descricao=descricao,
            fornecedor_id=fornecedor_id,
            pago=pago
        )

    def atualizar_boleto(self, boleto_id, codigo, vencimento, valor, tipo, descricao, fornecedor_id, status):
        return self.finance_repository.atualizar_boleto(
            boleto_id=boleto_id,
            codigo=codigo,
            vencimento=vencimento,
            valor=valor,
            tipo=tipo,
            descricao=descricao,
            fornecedor_id=fornecedor_id,
            status=status
        )

    def deletar_boleto(self, boleto_id: int):
        return self.finance_repository.deletar_boleto(boleto_id)

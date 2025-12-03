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
        # ... lógica para somar valores ...
        return {
            "a_vencer": 0.0,
            "vencidos": 0.0,
            "pagos": 0.0
        }

    def listar_boletos(self):
        return self.finance_repository.listar_boletos()

    def listar_notas_fiscais(self):
        return self.finance_repository.listar_notas_fiscais()

    def obter_nota_por_id(self, nota_id: int):
        return self.finance_repository.buscar_nota_por_id(nota_id)

    def atualizar_status_nota(self, nota_id: int, pago: bool):
        return self.finance_repository.atualizar_status_nota(nota_id, pago)

    def listar_fornecedores(self):
        return self.fornecedor_repository.listar_fornecedores()

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

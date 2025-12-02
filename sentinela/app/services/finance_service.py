from app.repositories.finance_repository import FinanceRepository

class FinanceService:
    def __init__(self):
        self.finance_repository = FinanceRepository()

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

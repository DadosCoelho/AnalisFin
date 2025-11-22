"""
Configurações do sistema AnalisFin
"""

from dataclasses import dataclass
from typing import Optional
from rich.console import Console
from rich.table import Table

console = Console()

@dataclass
class Config:
    """Classe de configuração do sistema"""
    
    # Parâmetros principais
    symbol: str = "BTCUSDT"
    period: str = "10min"
    qtd_consultas: int = 3
    qtd_periodo: int = 5
    
    # API
    api_provider: str = "binance"
    api_key: Optional[str] = None
    
    # Caminhos
    data_dir: str = "data/csvs"
    
    def update(self, **kwargs):
        """Atualiza configurações"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def display(self):
        """Exibe configurações atuais"""
        table = Table(title="Configurações Atuais")
        table.add_column("Parâmetro", style="cyan")
        table.add_column("Valor", style="green")
        
        table.add_row("Símbolo", self.symbol)
        table.add_row("Período", self.period)
        table.add_row("Consultas/Período", str(self.qtd_consultas))
        table.add_row("Quantidade de Períodos", str(self.qtd_periodo))
        table.add_row("API Provider", self.api_provider)
        
        console.print(table)
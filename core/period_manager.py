"""
Gerenciador de Períodos de Tempo
Calcula janelas de tempo com base nos parâmetros configurados
"""

from datetime import datetime, timedelta
from typing import List, Tuple
import re

class PeriodManager:
    """Gerencia cálculo de janelas de tempo"""
    
    def __init__(self, config):
        """
        Inicializa gerenciador de períodos
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
        self.period_duration = self._parse_period(config.period)
    
    def _parse_period(self, period_str: str) -> timedelta:
        """
        Converte string de período em timedelta
        
        Args:
            period_str: String como "10min", "1hora", "1dia"
            
        Returns:
            timedelta correspondente
        """
        # Regex para extrair número e unidade
        match = re.match(r'(\d+)\s*(min|hora|dia|semana|mes|ano)s?', period_str.lower())
        
        if not match:
            raise ValueError(f"Formato de período inválido: {period_str}")
        
        value = int(match.group(1))
        unit = match.group(2)
        
        # Mapeamento de unidades
        units = {
            'min': timedelta(minutes=value),
            'hora': timedelta(hours=value),
            'dia': timedelta(days=value),
            'semana': timedelta(weeks=value),
            'mes': timedelta(days=value * 30),  # Aproximação
            'ano': timedelta(days=value * 365)  # Aproximação
        }
        
        return units.get(unit, timedelta(minutes=value))
    
    def generate_periods(self) -> List[Tuple[datetime, datetime]]:
        """
        Gera lista de períodos a serem analisados
        
        Returns:
            Lista de tuplas (início, fim) para cada período
        """
        periods = []
        now = datetime.now()
        
        # Calcula períodos retroativamente
        for i in range(self.config.qtd_periodo):
            end_time = now - (self.period_duration * i)
            start_time = end_time - self.period_duration
            periods.append((start_time, end_time))
        
        # Inverte para ordem cronológica
        periods.reverse()
        
        return periods
"""
Agendador de Consultas
Divide cada período em consultas internas proporcionalmente
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class QueryScheduler:
    """Agenda consultas dentro de cada período"""
    
    def __init__(self, config):
        """
        Inicializa agendador
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
    
    def schedule_queries(self, periods: List[Tuple[datetime, datetime]]) -> List[Dict]:
        """
        Agenda consultas para todos os períodos
        
        Args:
            periods: Lista de tuplas (início, fim) de períodos
            
        Returns:
            Lista de dicionários com informações de cada consulta
        """
        all_queries = []
        
        for period_idx, (start, end) in enumerate(periods):
            queries = self._schedule_period(start, end, period_idx)
            all_queries.extend(queries)
        
        return all_queries
    
    def _schedule_period(self, start: datetime, end: datetime, 
                         period_idx: int) -> List[Dict]:
        """
        Agenda consultas dentro de um período específico
        
        Args:
            start: Início do período
            end: Fim do período
            period_idx: Índice do período
            
        Returns:
            Lista de consultas agendadas para este período
        """
        queries = []
        period_duration = end - start
        
        # Calcula intervalo entre consultas
        if self.config.qtd_consultas <= 1:
            interval = period_duration
        else:
            interval = period_duration / (self.config.qtd_consultas - 1)
        
        # Gera consultas
        for i in range(self.config.qtd_consultas):
            timestamp = start + (interval * i)
            
            # Garante que não ultrapasse o fim
            if timestamp > end:
                timestamp = end
            
            query = {
                'timestamp': timestamp,
                'period_idx': period_idx,
                'query_idx': i,
                'period_start': start,
                'period_end': end,
                'symbol': self.config.symbol,
                'percentage': (i / (self.config.qtd_consultas - 1)) * 100 if self.config.qtd_consultas > 1 else 0
            }
            
            queries.append(query)
        
        return queries
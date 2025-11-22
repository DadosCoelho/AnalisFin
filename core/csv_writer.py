"""
CSV Writer - Salva dados em arquivos CSV
Gera nomes únicos baseados em timestamp
"""

import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from typing import List, Dict

class CSVWriter:
    """Gerencia escrita de dados em CSV"""
    
    def __init__(self, config):
        """
        Inicializa writer
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Garante que diretório de dados existe"""
        Path(self.config.data_dir).mkdir(parents=True, exist_ok=True)
    
    def save(self, market_data: List[Dict]) -> str:
        """
        Salva dados em CSV
        
        Args:
            market_data: Lista de dados de mercado
            
        Returns:
            Caminho do arquivo CSV gerado
        """
        # Gera nome único com timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.csv"
        filepath = os.path.join(self.config.data_dir, filename)
        
        # Converte para DataFrame
        df = pd.DataFrame(market_data)
        
        # Ordena por período e consulta
        df = df.sort_values(['period_idx', 'query_idx'])
        
        # Formata timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Salva CSV
        df.to_csv(filepath, index=False)
        
        return filepath
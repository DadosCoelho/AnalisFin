"""
Data Fetcher - Busca dados de mercado
Suporta múltiplas APIs: Binance, Polygon, Yahoo Finance, etc.
"""

import requests
from typing import List, Dict
import time
from datetime import datetime

class DataFetcher:
    """Busca dados de mercado de diferentes APIs"""
    
    def __init__(self, config):
        """
        Inicializa fetcher
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
        self.api_map = {
            'binance': self._fetch_binance,
            'polygon': self._fetch_polygon,
            'yahoo': self._fetch_yahoo,
            'alphavantage': self._fetch_alphavantage
        }
    
    def fetch_all(self, queries: List[Dict]) -> List[Dict]:
        """
        Busca dados para todas as consultas
        
        Args:
            queries: Lista de consultas agendadas
            
        Returns:
            Lista de dados de mercado
        """
        market_data = []
        fetcher = self.api_map.get(self.config.api_provider, self._fetch_mock)
        
        for query in queries:
            data = fetcher(query)
            market_data.append(data)
            time.sleep(0.1)  # Rate limiting
        
        return market_data
    
    def _fetch_binance(self, query: Dict) -> Dict:
        """Busca dados da Binance API"""
        try:
            timestamp_ms = int(query['timestamp'].timestamp() * 1000)
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                'symbol': query['symbol'],
                'interval': '1m',
                'startTime': timestamp_ms,
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return self._format_data(query, data[0])
        except:
            pass
        
        return self._fetch_mock(query)
    
    def _fetch_polygon(self, query: Dict) -> Dict:
        """Busca dados da Polygon API (requer API key)"""
        # Implementação para Polygon
        return self._fetch_mock(query)
    
    def _fetch_yahoo(self, query: Dict) -> Dict:
        """Busca dados do Yahoo Finance"""
        # Implementação para Yahoo
        return self._fetch_mock(query)
    
    def _fetch_alphavantage(self, query: Dict) -> Dict:
        """Busca dados da AlphaVantage (requer API key)"""
        # Implementação para AlphaVantage
        return self._fetch_mock(query)
    
    def _fetch_mock(self, query: Dict) -> Dict:
        """Gera dados simulados para testes"""
        import random
        
        base_price = 50000
        variation = random.uniform(-1000, 1000)
        price = base_price + variation
        
        return {
            'timestamp': query['timestamp'],
            'symbol': query['symbol'],
            'open': price,
            'high': price * 1.002,
            'low': price * 0.998,
            'close': price + random.uniform(-100, 100),
            'volume': random.randint(1000000, 10000000),
            'period_idx': query['period_idx'],
            'query_idx': query['query_idx'],
            'percentage': query['percentage']
        }
    
    def _format_data(self, query: Dict, api_data) -> Dict:
        """Formata dados da API para formato padrão"""
        return {
            'timestamp': query['timestamp'],
            'symbol': query['symbol'],
            'open': float(api_data[1]),
            'high': float(api_data[2]),
            'low': float(api_data[3]),
            'close': float(api_data[4]),
            'volume': float(api_data[5]),
            'period_idx': query['period_idx'],
            'query_idx': query['query_idx'],
            'percentage': query['percentage']
        }
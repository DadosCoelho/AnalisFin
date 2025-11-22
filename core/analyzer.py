"""
Analyzer - Análise de tendências e cálculo de probabilidades
Implementa diversos indicadores técnicos
"""

import pandas as pd
import numpy as np
from typing import Dict

class Analyzer:
    """Analisa tendências de mercado"""
    
    def __init__(self, config):
        """
        Inicializa analisador
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
    
    def analyze(self, csv_path: str) -> Dict:
        """
        Analisa dados do CSV e retorna métricas
        
        Args:
            csv_path: Caminho do arquivo CSV
            
        Returns:
            Dicionário com análise completa
        """
        # Carrega dados
        df = pd.read_csv(csv_path)
        
        # Cálculos básicos
        trend_score = self._calculate_trend(df)
        prob_alta, prob_baixa = self._calculate_probabilities(df, trend_score)
        tendencia = self._classify_trend(trend_score)
        
        return {
            'curva': trend_score,
            'prob_alta': prob_alta,
            'prob_baixa': prob_baixa,
            'tendencia': tendencia,
            'arquivo_csv': csv_path
        }
    
    def _calculate_trend(self, df: pd.DataFrame) -> float:
        """
        Calcula curva de tendência (0-100)
        
        Args:
            df: DataFrame com dados
            
        Returns:
            Valor entre 0 (forte baixa) e 100 (forte alta)
        """
        # Média móvel simples
        df['sma'] = df['close'].rolling(window=min(3, len(df))).mean()
        
        # Direção da tendência
        if len(df) < 2:
            return 50.0
        
        first_price = df['close'].iloc[0]
        last_price = df['close'].iloc[-1]
        price_change = (last_price - first_price) / first_price
        
        # RSI simplificado
        rsi = self._calculate_rsi(df['close'])
        
        # Momentum
        momentum = self._calculate_momentum(df['close'])
        
        # Combina indicadores
        trend_score = 50  # Neutro
        trend_score += price_change * 100  # ±50
        trend_score += (rsi - 50) * 0.3  # ±15
        trend_score += momentum * 20  # ±20
        
        # Normaliza entre 0 e 100
        trend_score = max(0, min(100, trend_score))
        
        return trend_score
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """
        Calcula Índice de Força Relativa (RSI)
        
        Args:
            prices: Série de preços
            period: Período do RSI
            
        Returns:
            Valor RSI (0-100)
        """
        if len(prices) < 2:
            return 50.0
        
        deltas = prices.diff()
        gain = deltas.where(deltas > 0, 0).mean()
        loss = -deltas.where(deltas < 0, 0).mean()
        
        if loss == 0:
            return 100.0
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_momentum(self, prices: pd.Series) -> float:
        """
        Calcula momentum dos preços
        
        Args:
            prices: Série de preços
            
        Returns:
            Momentum normalizado (-1 a 1)
        """
        if len(prices) < 2:
            return 0.0
        
        momentum = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
        return np.tanh(momentum * 10)  # Normaliza
    
    def _calculate_probabilities(self, df: pd.DataFrame, trend_score: float) -> tuple:
        """
        Calcula probabilidades de alta e baixa
        
        Args:
            df: DataFrame com dados
            trend_score: Score de tendência
            
        Returns:
            Tupla (prob_alta, prob_baixa)
        """
        # Baseado na curva de tendência
        prob_alta = trend_score
        prob_baixa = 100 - trend_score
        
        # Ajusta com volatilidade
        volatility = df['close'].std() / df['close'].mean()
        confidence = max(0, 1 - volatility * 10)
        
        # Suaviza probabilidades baseado na confiança
        prob_alta = 50 + (prob_alta - 50) * confidence
        prob_baixa = 50 + (prob_baixa - 50) * confidence
        
        return prob_alta, prob_baixa
    
    def _classify_trend(self, trend_score: float) -> str:
        """
        Classifica tendência em categorias
        
        Args:
            trend_score: Score de tendência
            
        Returns:
            String: "alta", "baixa" ou "indefinido"
        """
        if trend_score > 60:
            return "alta"
        elif trend_score < 40:
            return "baixa"
        else:
            return "indefinido"
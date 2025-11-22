"""
Helpers - Funções auxiliares
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def list_csv_files():
    """Lista arquivos CSV salvos"""
    csv_dir = Path("data/csvs")
    if not csv_dir.exists():
        return []
    
    files = sorted([f.name for f in csv_dir.glob("*.csv")], reverse=True)
    return files

def generate_chart(csv_path: str):
    """
    Gera gráfico dos dados
    
    Args:
        csv_path: Caminho do CSV
    """
    df = pd.read_csv(csv_path)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close', linewidth=2)
    plt.plot(df.index, df['open'], label='Open', alpha=0.5)
    
    plt.title(f"Análise de {df['symbol'].iloc[0]}", fontsize=16)
    plt.xlabel("Consulta", fontsize=12)
    plt.ylabel("Preço", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = csv_path.replace('.csv', '.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Gráfico salvo: {output_path}")
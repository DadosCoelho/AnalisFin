# AnalisFin - Sistema de Análise de Mercado Financeiro

Sistema modular e escalável para análise de mercados financeiros com cálculo de tendências e probabilidades.

## 📋 Características

- ✅ Consultas periódicas configuráveis
- ✅ Suporte a múltiplas APIs (Binance, Polygon, Yahoo, AlphaVantage)
- ✅ Armazenamento em CSV com timestamps únicos
- ✅ Análise de tendências com RSI, momentum e médias móveis
- ✅ Cálculo de probabilidades (0-100)
- ✅ Interface CLI intuitiva
- ✅ Geração de gráficos

## 🚀 Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd analisfin

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

## 📦 Estrutura

```
analisfin/
├── main.py                 # Aplicação principal
├── requirements.txt
├── README.md
├── config/
│   └── settings.py        # Configurações
├── core/
│   ├── data_fetcher.py    # APIs de mercado
│   ├── period_manager.py  # Janelas de tempo
│   ├── query_scheduler.py # Agendamento
│   ├── csv_writer.py      # Persistência
│   └── analyzer.py        # Análise técnica
├── utils/
│   └── helpers.py         # Utilitários
└── data/
    └── csvs/              # CSVs gerados
```

## 💻 Uso

```bash
python main.py
```

### Menu Principal

1. **Configurar parâmetros** - Define período, consultas, etc.
2. **Executar análise** - Inicia coleta e análise
3. **Ver CSVs salvos** - Lista arquivos gerados
4. **Gerar gráficos** - Cria visualizações
5. **Sair**

### Parâmetros

- **periodo**: Duração da janela (ex: "10min", "1hora", "1dia")
- **qtd_consultas**: Pontos de coleta por período (ex: 3, 5, 10)
- **qtd_periodo**: Quantos períodos analisar (ex: 5, 10, 100)
- **symbol**: Ativo financeiro (ex: "BTCUSDT", "AAPL")
- **api_provider**: API a usar (binance, polygon, yahoo, alphavantage)

## 📊 Exemplo

```python
periodo = "10min"
qtd_consultas = 3
qtd_periodo = 5
symbol = "BTCUSDT"

# Resultado:
# - Analisa últimos 5 períodos de 10min
# - 3 consultas por período = 15 consultas totais
# - Gera CSV único
# - Calcula probabilidades
```

## 🔬 Análise Técnica

O sistema calcula:

1. **Curva de Tendência (0-100)**
   - 0-40: Tendência de baixa
   - 40-60: Indefinido
   - 60-100: Tendência de alta

2. **Probabilidades**
   - prob_alta: Chance de valorização
   - prob_baixa: Chance de desvalorização

3. **Indicadores**
   - RSI (Relative Strength Index)
   - Momentum
   - Médias Móveis

## 📈 Output

```json
{
  "curva": 67.5,
  "prob_alta": 67.5,
  "prob_baixa": 32.5,
  "tendencia": "alta",
  "arquivo_csv": "data/csvs/2025-11-22_15-30-00.csv"
}
```

## 🔑 APIs

### Binance (Padrão)
- Sem necessidade de API key
- Limite de rate: 1200 req/min

### Outras APIs
Configure `api_key` em `config/settings.py` para:
- Polygon.io
- AlphaVantage
- Yahoo Finance

## 🛠️ Desenvolvimento

### Adicionar Nova API

1. Edite `core/data_fetcher.py`
2. Implemente método `_fetch_suaapi()`
3. Adicione ao `api_map`

### Novos Indicadores

1. Edite `core/analyzer.py`
2. Adicione método de cálculo
3. Integre em `_calculate_trend()`

## 📝 Formato CSV

```csv
timestamp,symbol,open,high,low,close,volume,period_idx,query_idx,percentage
2025-11-22 15:00:00,BTCUSDT,50000,50100,49900,50050,1000000,0,0,0.0
2025-11-22 15:05:00,BTCUSDT,50050,50200,50000,50150,1200000,0,1,50.0
...
```

## 🎯 Melhorias Futuras

- [ ] Machine Learning para previsões
- [ ] Backtesting automático
- [ ] Alertas em tempo real
- [ ] Dashboard web
- [ ] Suporte a múltiplos símbolos simultâneos
- [ ] Cache de dados
- [ ] Exportação para outros formatos (JSON, Excel)

## 📄 Licença

MIT License

## 👤 Autor

Sistema AnalisFin - Análise Financeira Automatizada
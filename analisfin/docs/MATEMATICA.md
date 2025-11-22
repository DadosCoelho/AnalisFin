# Explicação Matemática - AnalisFin

## 1. Cálculo da Curva de Tendência

A curva de tendência é calculada como uma composição ponderada de múltiplos indicadores técnicos, normalizada em uma escala de 0 a 100.

### Fórmula Geral

```
Curva = Base + ΔPreço + RSI_adj + Momentum_adj
```

Onde:
- **Base = 50** (ponto neutro)
- **ΔPreço**: Variação percentual do preço
- **RSI_adj**: Ajuste baseado no RSI
- **Momentum_adj**: Ajuste baseado no momentum

### 1.1 Variação de Preço

```
ΔPreço = ((P_final - P_inicial) / P_inicial) × 100
```

Contribui com ±50 pontos para a curva.

### 1.2 RSI (Relative Strength Index)

```
RSI = 100 - (100 / (1 + RS))

Onde:
RS = Média dos Ganhos / Média das Perdas
```

**Ajuste para Curva:**
```
RSI_adj = (RSI - 50) × 0.3
```

Contribui com ±15 pontos.

**Interpretação:**
- RSI > 70: Sobrecomprado (pressão de venda)
- RSI < 30: Sobrevendido (pressão de compra)
- RSI ≈ 50: Neutro

### 1.3 Momentum

```
Momentum_raw = (P_final - P_inicial) / P_inicial

Momentum_norm = tanh(Momentum_raw × 10)
```

A função tangente hiperbólica normaliza o momentum entre -1 e 1.

**Ajuste para Curva:**
```
Momentum_adj = Momentum_norm × 20
```

Contribui com ±20 pontos.

### 1.4 Normalização Final

```
Curva_final = max(0, min(100, Curva))
```

Garante que o valor fique entre 0 e 100.

## 2. Cálculo de Probabilidades

### 2.1 Probabilidades Base

```
P_alta_base = Curva
P_baixa_base = 100 - Curva
```

### 2.2 Ajuste por Volatilidade

A volatilidade reduz a confiança nas probabilidades extremas.

```
Volatilidade = σ(preços) / μ(preços)

Confiança = max(0, 1 - Volatilidade × 10)
```

Onde:
- σ = desvio padrão
- μ = média

### 2.3 Probabilidades Ajustadas

```
P_alta = 50 + (P_alta_base - 50) × Confiança
P_baixa = 50 + (P_baixa_base - 50) × Confiança
```

**Efeito:**
- Alta volatilidade → Probabilidades se aproximam de 50/50
- Baixa volatilidade → Probabilidades mais extremas

## 3. Média Móvel Simples (SMA)

```
SMA_n = (Σ P_i) / n

Para i = t-n+1 até t
```

Onde:
- n = janela da média
- P_i = preço no instante i

**Uso:** Suaviza ruído e identifica tendências de médio prazo.

## 4. Distribuição de Consultas

Para dividir um período em consultas igualmente espaçadas:

```
Δt = Duração_período / (n_consultas - 1)

t_i = t_início + (Δt × i)

Para i = 0, 1, 2, ..., n_consultas-1
```

**Percentual de Progresso:**
```
Percentual_i = (i / (n_consultas - 1)) × 100
```

## 5. Exemplo Numérico

### Dados:
- P_inicial = 50000
- P_final = 51000
- RSI = 65
- Período = 10 períodos

### Cálculo:

**1. Variação de Preço:**
```
ΔPreço = ((51000 - 50000) / 50000) × 100 = 2%
Contribuição = 2 × 50 = 100 pontos
```

**2. RSI Ajustado:**
```
RSI_adj = (65 - 50) × 0.3 = 4.5 pontos
```

**3. Momentum:**
```
Momentum_raw = 0.02
Momentum_norm = tanh(0.02 × 10) = tanh(0.2) ≈ 0.197
Momentum_adj = 0.197 × 20 = 3.94 pontos
```

**4. Curva Final:**
```
Curva = 50 + 100 + 4.5 + 3.94 = 158.44
Curva_final = min(100, 158.44) = 100
```

**5. Probabilidades:**

Assumindo volatilidade de 2%:
```
Confiança = max(0, 1 - 0.02 × 10) = 0.8

P_alta = 50 + (100 - 50) × 0.8 = 90%
P_baixa = 50 + (0 - 50) × 0.8 = 10%
```

## 6. Limitações e Considerações

### 6.1 Overfitting
Os pesos (×100, ×0.3, ×20) são empíricos e devem ser ajustados com backtesting.

### 6.2 Look-Ahead Bias
Todos os cálculos usam apenas dados históricos disponíveis no momento da análise.

### 6.3 Mercados Eficientes
Em mercados eficientes, padrões técnicos podem ter poder preditivo limitado.

### 6.4 Eventos Externos
O modelo não considera notícias, eventos macroeconômicos ou mudanças fundamentais.

## 7. Melhorias Matemáticas

### 7.1 Machine Learning
```
P(alta) = σ(w₁·RSI + w₂·Momentum + w₃·SMA + ... + b)
```

Onde σ = sigmoid, w = pesos aprendidos, b = bias.

### 7.2 Análise de Fourier
Decomposição de séries temporais para identificar ciclos:
```
f(t) = Σ [a_n·cos(nωt) + b_n·sin(nωt)]
```

### 7.3 GARCH
Modelagem de volatilidade condicional:
```
σ²_t = ω + α·ε²_(t-1) + β·σ²_(t-1)
```

### 7.4 Redes LSTM
Para capturar dependências temporais de longo prazo em séries financeiras.

## Referências

1. Wilder, J. W. (1978). New Concepts in Technical Trading Systems
2. Murphy, J. J. (1999). Technical Analysis of the Financial Markets
3. Tsay, R. S. (2010). Analysis of Financial Time Series
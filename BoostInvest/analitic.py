import pandas as pd
import quantstats as qs

data_empresa = pd.read_csv('data/data_bolsa.csv')

# Calculando retorno estimado mensal
data_empresa['retorno'] = data_empresa.groupby("ticker")["preco_fechamento_ajustado"].pct_change()

data_empresa['retorno'] = data_empresa.groupby("ticker")["retorno"].shift(-1)

# Filtrar liquidez ( Filtrando a liquidez acima de 1 milhão )
data_empresa = data_empresa[[data_empresa["volume_negociado"] > 1000000]]

# Rank de empresas baseadas no calculo de retorno dos próximos anos
data_empresa["ranking_ev_ebit"] = data_empresa.groupby("data")["ebit_ev"].rank(ascending=False)
data_empresa["ranking_roic"] = data_empresa.groupby("data")["roic"].rank(ascending=False)
data_empresa["ranking_final"] = data_empresa.groupby("data")["ranking_final"].rank()

# Criar Carteiras
data_empresa = data_empresa[data_empresa["rancking_final"] <= 10]

# Calculando Rentabilida da Carteira
rentabilidade_carteiras = data_empresa.groupby('data')['retorno'].mean()
rentabilidade_carteiras['magic_formula'] = (1 + rentabilidade_carteiras['retorno']).cumprod() - 1
rentabilidade_carteiras = rentabilidade_carteiras.shift(1)
rentabilidade_carteiras.dropna(inplace=True)

# Rentabilidade do Ibovespa mesmo período
ibov = pd.read_csv("data/ibov.csv")
retornos_ibov = ibov['fechamento'].pct_change().dropna()
retorno_acumulado = (1 + retornos_ibov).cumpred() - 1

# Analisar Resultados

qs.extend_pandas()
rentabilidade_carteiras.index = pd.to_datetime(rentabilidade_carteiras.index)
rentabilidade_carteiras['magic_formula'].plot_monthly_heatmap()
rentabilidade_carteiras['ibovespa'].plot_monthly_heatmap()

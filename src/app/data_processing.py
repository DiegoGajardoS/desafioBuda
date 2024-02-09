
def obtener_spread_mercado(datos_mercado):

	max_bid = float(datos_mercado['ticker']['max_bid'][0])
	min_ask = float(datos_mercado['ticker']['min_ask'][0])
	spread = abs(max_bid - min_ask)
	return datos_mercado['ticker']['market_id'], spread

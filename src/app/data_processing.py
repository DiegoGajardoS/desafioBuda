import json

def obtener_spread_mercado(datos_mercado):

	max_bid = float(datos_mercado['ticker']['max_bid'][0])
	min_ask = float(datos_mercado['ticker']['min_ask'][0])
	spread = abs(max_bid - min_ask)

	data = (datos_mercado['ticker']['market_id'],spread)
	json_data = {'market-id': data[0], 'spread': data[1]}
	json_string = json.dumps(json_data)
	return json_string

def obtener_idMercados(mercados):
	cant_mercados = len(mercados['tickers'])
	markets_id = []
	i=0
	while i < cant_mercados:
		market_id = mercados['tickers'][i]['market_id']
		markets_id.append(market_id)
		i=i+1
	return markets_id


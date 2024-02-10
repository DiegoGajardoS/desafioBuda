#Bloque de importaciones
import json

#Funcionalidades

# Entrada: Diccionario con los datos de un mercado 
# Salida: Diccionario con el market_id y el spread del mercado
# La función se encarga de encontrar el spread (la diferencia entre la orden de venta más barata y la orden de compra más cara) del mercado
def obtener_spread_mercado(datos_mercado):

	max_bid = float(datos_mercado['ticker']['max_bid'][0])
	min_ask = float(datos_mercado['ticker']['min_ask'][0])
	spread = abs(max_bid - min_ask)

	data = (datos_mercado['ticker']['market_id'],spread)
	json_data = {'market_id': data[0], 'spread': data[1]}
	json_string = json.dumps(json_data)
	return json_string

# Entrada: Diccionario con los datos de todos los mercados disponibles
# Salida: Una lista de markets_id
# La función se encarga de encontrar los id de todos los mercados disponibles 
def obtener_idMercados(mercados):
	cant_mercados = len(mercados['markets'])
	markets_id = []
	i=0
	while i < cant_mercados:
		market_id = mercados['markets'][i]['id']
		markets_id.append(market_id)
		i=i+1
	return markets_id


#Bloque de importaciones

import requests

#Funcionalidades

# Entrada: String market_id
# Salida: Diccionario con los datos del mercado buscado, o diccionario con mensaje de error
# La función se encarga de extraer los datos de un mercado en específico desde la api de buda.com mediante una llamada pública  
def obtener_datos_mercado(mercado):
	#convierto el string en mayúscula
	mercadoUpper = mercado.upper()
	#realizo la llamada pública a la API de buda
	url = f'https://www.buda.com/api/v2/markets/{mercadoUpper}/ticker'
	#almaceno la respuesta
	response = requests.get(url)
	if response.status_code == 200:
		#retorno la respuesta
		return response.json()
	#en caso de no encontrar los datos del mercado retorno un error
	else:
		return {'error', 'no se logran obtener los datos de este mercado'}

# Entrada: No posee
# Salida: Diccionario con la lista de todos los mercados encontrados
# La función se encarga de extraer la lista de todos los mercados desde la api de buda.com mediante una llamada pública  
def obtener_mercados():
	#realizo la llamada pública a la API de buda
	url = f'https://www.buda.com/api/v2/markets'
	#almaceno la respuesta
	response = requests.get(url)
	#en caso de tener respuesta, la retorno
	if response.status_code == 200:
		return response.json()
	#en caso contrario retorno un error
	else:
		return {'error', 'no se logran obtener los datos de los mercados'}


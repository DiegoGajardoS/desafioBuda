import requests

def obtener_datos_mercado(mercado):

	url = f'https://www.buda.com/api/v2/markets/{mercado}/ticker'
	response = requests.get(url)
	
	if response.status_code == 200:
		return response.json()
	else:
		return {'error', 'no se logran obtener los datos de este mercado'}

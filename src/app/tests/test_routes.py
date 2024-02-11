'''import json
from ...run import apk

# Define datos de prueba
valid_market_id = 'BTC-CLP'
invalid_market_id = 'INVALID-MARKET'

# Prueba para verificar si se puede obtener el spread de un mercado válido
def test_spread_mercado_valido():
    # Crear un cliente de prueba para hacer solicitudes HTTP
    client = apk.test_client()

    # Realizar la solicitud GET a la ruta de la API con un mercado válido
    response = client.get(f'/spread/{valid_market_id}')

    # Verificar el código de estado de la respuesta
    assert response.status_code == 200

    # Verificar si la respuesta contiene el spread y el market_id
    data = json.loads(response.data)
    assert 'spread' in data
    assert 'market_id' in data

# Prueba para verificar si se maneja correctamente un mercado no válido
def test_spread_mercado_no_valido():
    # Crear un cliente de prueba para hacer solicitudes HTTP
    client = apk.test_client()

    # Realizar la solicitud GET a la ruta de la API con un mercado no válido
    response = client.get(f'/spread/{invalid_market_id}')

    # Verificar el código de estado de la respuesta
    assert response.status_code == 500

    # Verificar si la respuesta contiene un mensaje de error
    data = json.loads(response.data)
    assert 'error' in data
'''
import json
from ..test_run import app
from unittest.mock import patch
import pytest

#TEST PARA LA RUTA /spread/<mercado>'
# se definen datos de prueba
valid_market_id = 'BTC-CLP'
invalid_market_id = 'INVALID-MARKET'

# prueba para verificar si se puede obtener el spread de un mercado válido
def test_spread_mercado_valido():
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()

    # realizar la solicitud GET a la ruta de la API con un mercado válido
    response = client.get(f'/spread/{valid_market_id}')

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar si la respuesta contiene el spread y el market_id
    data = json.loads(response.data)
    assert 'spread' in data
    assert 'market_id' in data

# prueba para verificar un mercado no válido
def test_spread_mercado_no_valido():
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()

    # realizar la solicitud GET a la ruta de la API con un mercado no válido
    response = client.get(f'/spread/{invalid_market_id}')

    # verificar el código de estado de la respuesta
    assert response.status_code == 500

    # verificar si la respuesta contiene un mensaje de error
    data = json.loads(response.data)
    assert 'error' in data

#TEST PARA LA RUTA /spread

def test_getMercados():

    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread')

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar si la respuesta contiene los spreads de todos los mercados
    data = json.loads(response.data)
    # verificar cada elemento en la lista data
    for item in data:
        assert 'spread' in item
        assert 'market_id' in item

# prueba para verificar si se maneja correctamente el error al no obtener datos de los mercados
# mock de la función obtener_mercados
def mock_obtener_mercados():
    return [{'market_id': 'BTC-CLP'}, {'market_id': 'ETH-CLP'}]

@patch('app.routes.obtener_mercados', return_value={'error', 'no se logran obtener los datos de los mercados'})
def test_getMercados_error(mock_obtener_mercados):

    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread')
    # verificar el código de estado de la respuesta
    assert response.status_code == 500
    # verificar si la respuesta contiene un mensaje de error
    data = json.loads(response.data)
    assert 'error' in data

#TEST PARA LA RUTA /spread/alerta'
# prueba para verificar si se puede crear un nuevo spread de alerta correctamente
def test_guardar_spread_nuevo():
    # datos de prueba
    new_spread_data = {'market_id': 'BTC-CLP', 'spread': 1000}
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud POST a la ruta de la API
    response = client.post('/spread/alerta', json=new_spread_data)

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'Spread de alerta guardado correctamente'

# prueba para verificar si se puede actualizar un spread de alerta existente correctamente
def test_actualizar_spread_existente():
    # datos de prueba
    existing_spread_data = {'market_id': 'BTC-CLP', 'spread': 2000}
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud POST a la ruta de la API
    response = client.post('/spread/alerta', json=existing_spread_data)

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'Spread de alerta actualizado correctamente'

# prueba para verificar si se maneja correctamente un JSON incompleto
def test_json_incompleto():
    # datos de prueba con JSON incompleto
    incomplete_data = {'market_id': 'BTC-CLP'}
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud POST a la ruta de la API
    response = client.post('/spread/alerta', json=incomplete_data)

    # verificar el código de estado de la respuesta
    assert response.status_code == 400

    # verificar el mensaje de error
    data = json.loads(response.data)
    assert data['error'] == 'El JSON enviado no contiene market_id o spread'

#TEST PARA LA RUTA /spread/alerta/<mercado>

# mock de la función encontrar_spread
def mock_encontrar_spread(spreads, market_id):
    if market_id == 'BTC-CLP':
        return (True, 1000)
    elif market_id == 'ETH-CLP':
        return (True, 2000)  
    elif market_id == 'LTC-BTC':
        return (True, 8000)  
    else:
        return (False, None)

# mock de la función spread_mercado
def mock_spread_mercado(mercado):
    if mercado == 'BTC-CLP':
        return {'spread': 1500} 
    elif mercado == 'ETH-CLP':
        return {'spread': 1500}  
    elif mercado == 'LTC-BTC':
        return {'spread':8000}
    else:
        return {'spread': None}

# prueba para verificar si se puede consultar el spread de alerta correctamente cuando el spread actual es mayor
@patch('app.routes.encontrar_spread', side_effect=mock_encontrar_spread)
@patch('app.routes.spread_mercado', side_effect=mock_spread_mercado)
def test_consultar_spread_alerta_spread_mayor(mock_encontrar_spread, mock_spread_mercado):
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread/alerta/BTC-CLP')

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'El spread actual es mayor al spread guardado'
    assert data['spread actual'] == 1500
    assert data['spread guardado'] == 1000
    assert data['market_id'] == 'BTC-CLP'

# prueba para verificar si se puede consultar el spread de alerta correctamente cuando el spread actual es menor
@patch('app.routes.encontrar_spread', side_effect=mock_encontrar_spread)
@patch('app.routes.spread_mercado', side_effect=mock_spread_mercado)
def test_consultar_spread_alerta_spread_menor(mock_encontrar_spread, mock_spread_mercado):
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread/alerta/ETH-CLP')
    # verificar el código de estado de la respuesta
    assert response.status_code == 200
    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'El spread actual es menor al spread guardado'
    assert data['spread actual'] == 1500
    assert data['spread guardado'] == 2000
    assert data['market_id'] == 'ETH-CLP'

# prueba para verificar si se puede consultar el spread de alerta correctamente cuando el spread actual es igual
@patch('app.routes.encontrar_spread', side_effect=mock_encontrar_spread)
@patch('app.routes.spread_mercado', side_effect=mock_spread_mercado)
def test_consultar_spread_alerta_spread_igual(mock_encontrar_spread, mock_spread_mercado):
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread/alerta/LTC-BTC')

    # verificar el código de estado de la respuesta
    assert response.status_code == 200

    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'El spread actual es igual al spread guardado'
    assert data['spread actual'] == 8000
    assert data['spread guardado'] == 8000
    assert data['market_id'] == 'LTC-BTC'

# prueba para verificar si se maneja correctamente cuando no hay spread guardado para el mercado
@patch('app.routes.encontrar_spread', side_effect=mock_encontrar_spread)
def test_consultar_spread_alerta_sin_spread(mock_encontrar_spread):
    # crear un cliente de prueba para hacer solicitudes HTTP
    client = app.test_client()
    # realizar la solicitud GET a la ruta de la API
    response = client.get('/spread/alerta/X')

    # verificar el código de estado de la respuesta
    assert response.status_code == 404

    # verificar el mensaje de respuesta
    data = json.loads(response.data)
    assert data['mensaje'] == 'No hay spread guardado para este mercado'
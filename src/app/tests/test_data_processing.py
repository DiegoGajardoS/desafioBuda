import pytest
import json
from ..data_processing import obtener_spread_mercado
from ..data_processing import obtener_idMercados
from ..data_processing import guardar_spread_alerta
from ..data_processing import encontrar_spread


#TEST FUNCION PARA OBTENER SPREAD DE X MERCADO
@pytest.mark.parametrize("datos_mercado, expected_result", [
	# caso de prueba con max_bid mayor al min_ask
    (
        {'ticker': {'market_id': 'BTC-CLP', 'max_bid': [100], 'min_ask': [90]}},
        {'market_id': 'BTC-CLP', 'spread': 10}
    ),
    # caso de prueba con max_bid menor al min_ask
    (
        {'ticker': {'market_id': 'ETH-CLP', 'max_bid': [80], 'min_ask': [85]}},
        {'market_id': 'ETH-CLP', 'spread': 5}
    ),  
    # caso de prueba con max_bid igual al min_ask
    (
        {'ticker': {'market_id': 'BTC-CLP', 'max_bid': [100], 'min_ask': [100]}},
        {'market_id': 'BTC-CLP', 'spread': 0}
    ),  
])
def test_obtener_spread_mercado(datos_mercado, expected_result):
    # se llama a la funcion a probar
    resultado = json.loads(obtener_spread_mercado(datos_mercado))

    # se comprueba el resultado
    assert resultado == expected_result

#TEST FUNCION PARA OBTENER LOS ID DE LOS MERCADOS
# datos de entrada esperados
mercados_entrada = {'markets': [{'id': 'BTC-CLP'}, {'id': 'ETH-CLP'}, {'id': 'LTC-CLP'}]}
# resultado esperado para la prueba
ids_esperados = ['BTC-CLP', 'ETH-CLP', 'LTC-CLP']

def test_obtener_idMercados():
    # se llama a la funcion a probar
    ids_obtenidos = obtener_idMercados(mercados_entrada)

    # se comprueba el resultado
    assert ids_obtenidos == ids_esperados

#TEST FUNCION PARA GUARDAR UN SPREAD DE ALERTA
@pytest.fixture
def spreads_alerta_inicial():
    return [{'market_id': 'BTC-CLP', 'spread': 5.0}, {'market_id': 'ETH-CLP', 'spread': 10.0}]

def test_actualizar_spread_existente(spreads_alerta_inicial):
    spreads_alerta = spreads_alerta_inicial[:]
    market_id = 'BTC-CLP'
    spread_nuevo = 7.0
    resultado = guardar_spread_alerta(spreads_alerta, market_id, spread_nuevo)
    assert resultado == True
    assert spreads_alerta == [{'market_id': 'BTC-CLP', 'spread': 7.0}, {'market_id': 'ETH-CLP', 'spread': 10.0}]

def test_agregar_nuevo_spread(spreads_alerta_inicial):
    spreads_alerta = spreads_alerta_inicial[:]
    market_id = 'LTC-CLP'
    spread_nuevo = 8.0
    resultado = guardar_spread_alerta(spreads_alerta, market_id, spread_nuevo)
    assert resultado == False
    assert spreads_alerta == [{'market_id': 'BTC-CLP', 'spread': 5.0}, {'market_id': 'ETH-CLP', 'spread': 10.0}, {'market_id': 'LTC-CLP', 'spread': 8.0}]

def test_retorno_true_actualizacion_existente():
    spreads_alerta = [{'market_id': 'BTC-CLP', 'spread': 5.0}]
    market_id = 'btc-clp'
    spread_nuevo = 7.0
    resultado = guardar_spread_alerta(spreads_alerta, market_id, spread_nuevo)
    assert resultado == True

def test_retorno_false_agregar_nuevo():
    spreads_alerta = [{'market_id': 'BTC-CLP', 'spread': 5.0}]
    market_id = 'eth-clp'
    spread_nuevo = 10.0
    resultado = guardar_spread_alerta(spreads_alerta, market_id, spread_nuevo)
    assert resultado == False


#TEST FUNCION PARA ENCONTRAR UN SPREAD
@pytest.fixture
def spreads_alerta_inicial():
    return [{'market_id': 'BTC-CLP', 'spread': 5.0}, {'market_id': 'ETH-CLP', 'spread': 10.0}]

def test_encontrar_spread_existente(spreads_alerta_inicial):
    spreads_alerta = spreads_alerta_inicial[:]
    market_id = 'BTC-CLP'
    resultado = encontrar_spread(spreads_alerta, market_id)
    assert resultado == [True, 5.0]

def test_encontrar_spread_no_existente(spreads_alerta_inicial):
    spreads_alerta = spreads_alerta_inicial[:]
    market_id = 'LTC-CLP'
    resultado = encontrar_spread(spreads_alerta, market_id)
    assert resultado == [False, None]

def test_valores_correctos_si_encontrado():
    spreads_alerta = [{'market_id': 'BTC-CLP', 'spread': 5.0}]
    market_id = 'BTC-CLP'
    resultado = encontrar_spread(spreads_alerta, market_id)
    assert resultado == [True, 5.0]

def test_valores_correctos_si_no_encontrado():
    spreads_alerta = [{'market_id': 'BTC-CLP', 'spread': 5.0}]
    market_id = 'ETH-CLP'
    resultado = encontrar_spread(spreads_alerta, market_id)
    assert resultado == [False, None]
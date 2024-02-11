import pytest
from unittest.mock import patch
from ..api import obtener_datos_mercado
from ..api import obtener_mercados


# datos de mercado esperados para mercado válido
datos_mercado_esperados = {'market_id': 'BTC-CLP'}

# datos de mercado esperados para mercado no válido
datos_mercado_no_valido = {'error', 'no se logran obtener los datos de este mercado'}

@pytest.mark.parametrize("status_code, mercado, expected_result", [
    (200, 'BTC-CLP', datos_mercado_esperados), 
    (404, 'XXX-CLP', datos_mercado_no_valido)   
])
@patch('app.api.requests.get')  
def test_obtener_datos_mercado(mock_get, status_code, mercado, expected_result):
    # se configura el comportamiento simulado de requests.get
    mock_response = mock_get.return_value
    mock_response.status_code = status_code
    if status_code == 200:
        mock_response.json.return_value = expected_result  
    else:
        mock_response.json.return_value = {}  

    # se llama a la función a probar
    resultado = obtener_datos_mercado(mercado)

    # se comprueba el resultado
    assert resultado == expected_result

@pytest.mark.parametrize("status_code, expected_result", [
    (200, [{'market_id': 'BTC-CLP'}, {'market_id': 'ETH-CLP'}])])
@patch('app.api.requests.get')  
def test_obtener_mercados(mock_get, status_code, expected_result):
    # Configuramos el comportamiento simulado de requests.get
    mock_response = mock_get.return_value
    mock_response.status_code = status_code
    if status_code == 200:
        mock_response.json.return_value = [{'market_id': 'BTC-CLP'}, {'market_id': 'ETH-CLP'}]  
    else:
        mock_response.json.return_value = {}  

    # Llamamos a la función que queremos probar
    resultado = obtener_mercados()

    # Comprobamos si el resultado es el esperado
    assert resultado == expected_result
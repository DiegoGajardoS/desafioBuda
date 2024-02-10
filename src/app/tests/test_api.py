import pytest
from unittest.mock import patch
from app.api import obtener_datos_mercado
from app.api import obtener_mercados


# Creamos un diccionario con los datos de mercado esperados
datos_mercado_esperados = {'market_id': 'BTC-CLP'}

@pytest.mark.parametrize("status_code, expected_result", [
    (200, datos_mercado_esperados)])
@patch('app.api.requests.get')  
def test_obtener_datos_mercado(mock_get, status_code, expected_result):
    # Configuramos el comportamiento simulado de requests.get
    mock_response = mock_get.return_value
    mock_response.status_code = status_code
    if status_code == 200:
        mock_response.json.return_value = datos_mercado_esperados  
    else:
        mock_response.json.return_value = {}  

    # Llamamos a la función que queremos probar
    resultado = obtener_datos_mercado('BTC-CLP')

    # Comprobamos si el resultado es el esperado
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
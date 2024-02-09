from flask import Blueprint, jsonify
from app.api import obtener_datos_mercado
from app.api import obtener_mercados
from app.data_processing import obtener_spread_mercado
from app.data_processing import obtener_idMercados

bp = Blueprint('api', __name__)

@bp.route('/spread/<mercado>', methods=['GET'])
def spread_mercado(mercado):
    datos_mercado = obtener_datos_mercado(mercado)
    if datos_mercado:
        spread = obtener_spread_mercado(datos_mercado)
        return jsonify(spread)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500

@bp.route('/spread', methods=['GET'])
def getMercados():
    spreads = []
    mercados = obtener_mercados()
    if mercados:
        ids = obtener_idMercados(mercados)
        i = 0
        while i < len(ids):
            datos_mercado = obtener_datos_mercado(ids[i])
            if datos_mercado:
                spread = obtener_spread_mercado(datos_mercado)
                spreads.append(spread)
                i=i+1
            else:
                return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500
        return spreads
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500

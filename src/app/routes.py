from flask import Blueprint, jsonify
from app.api import obtener_datos_mercado
from app.data_processing import obtener_spread_mercado

bp = Blueprint('api', __name__)

@bp.route('/spread/<mercado>', methods=['GET'])
def spread_mercado(mercado):
    datos_mercado = obtener_datos_mercado(mercado)
    if datos_mercado:
        spread = obtener_spread_mercado(datos_mercado)
        return jsonify(spread)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500

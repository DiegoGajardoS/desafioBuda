from flask import Blueprint, jsonify, request
from app.api import obtener_datos_mercado
from app.api import obtener_mercados
from app.data_processing import obtener_spread_mercado
from app.data_processing import obtener_idMercados
from app.globals import spreads_alerta
import json
bp = Blueprint('api', __name__)

@bp.route('/spread/<mercado>', methods=['GET'])
def spread_mercado(mercado):
    datos_mercado = obtener_datos_mercado(mercado)
    if datos_mercado:
        spread = obtener_spread_mercado(datos_mercado)
        spread_dict = json.loads(spread)
        return spread_dict
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
                spread_dict = json.loads(spread) 
                spreads.append(spread_dict) 
                i=i+1
            else:
                return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500
        return jsonify(spreads)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500

@bp.route('/spread/alerta', methods=['POST'])
def guardar_spread():
    global spreads_alerta
    data = request.json
    market_id = data.get('market_id')
    spread_nuevo = data.get('spread')

    if market_id is None or spread_nuevo is None:
        return jsonify({'error': 'El JSON enviado no contiene market_id o spread'}), 400

    else:
        val = True;
        mercadoUpper = market_id.upper()
        for spread in spreads_alerta:
            if spread['market_id'] == mercadoUpper:
                spread['spread'] = spread_nuevo
                val = False
                return jsonify({'mensaje': 'Spread de alerta actualizado correctamente'}), 200
        if val: 
            spreads_alerta.append({'market_id': mercadoUpper, 'spread': spread_nuevo})
            return jsonify({'mensaje': 'Spread de alerta guardado correctamente'}), 200

@bp.route('/spread/alerta/<mercado>', methods=['GET'])
def consultar_spread_alerta(mercado):
    global spreads_alerta
    if not spreads_alerta:
         return jsonify({'mensaje': 'No se han establecido spreads de alerta'}), 404
    spread_guardado = 0
    encontrado = False
    for spread in spreads_alerta:
        mercadoUpper = mercado.upper()
        if spread['market_id'] == mercadoUpper:
            encontrado = True
            spread_guardado = float(spread['spread'])

    if encontrado:
           spread_actual = spread_mercado(mercado)
           print(spread_actual)
           valor_spread_actual = spread_actual['spread']

           print(valor_spread_actual)
           if valor_spread_actual > spread_guardado:
             return jsonify({'mensaje': 'El spread actual es mayor al spread guardado',
                             'spread actual': valor_spread_actual,
                             'spread guardado': spread_guardado,
                             'market_id': mercadoUpper }), 200
           if valor_spread_actual < spread_guardado:
             return jsonify({'mensaje': 'El spread actual es menor al spread guardado',
                             'spread actual': valor_spread_actual,
                             'spread guardado': spread_guardado,
                             'market_id': mercadoUpper }), 200
           if valor_spread_actual == spread_guardado:
             return jsonify({'mensaje': 'El spread actual es igual al spread guardado',
                             'spread actual': valor_spread_actual,
                             'spread guardado': spread_guardado,
                             'market_id': mercadoUpper }), 200
    else:

        return jsonify({'mensaje': 'No hay spread guardado para este mercado'}), 404
    


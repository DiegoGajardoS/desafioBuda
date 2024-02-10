#Bloque de importaciones

from flask import Blueprint, jsonify, request
from app.api import obtener_datos_mercado
from app.api import obtener_mercados
from app.data_processing import obtener_spread_mercado
from app.data_processing import obtener_idMercados
from app.data_processing import guardar_spread_alerta
from app.data_processing import encontrar_spread
from app.globals import spreads_alerta

import json

# Se crea un Blueprint llamado 'api' que se utilizará para definir las rutas relacionadas con la API.
# Este Blueprint se asocia con el nombre del módulo actual (__name__) para asegurar que las rutas sean registradas correctamente.
bp = Blueprint('api', __name__)

#Rutas

#Ruta para obtener el spread de un mercado específico
#Entrada: recibe como string el 'mercado', el cual es el market_id del mercado a buscar
#Salida: retorna un diccionario con el spread y el market_id del mercado, o un mensaje de error
@bp.route('/spread/<mercado>', methods=['GET'])
def spread_mercado(mercado):
    datos_mercado = obtener_datos_mercado(mercado)
    if datos_mercado:
        spread = obtener_spread_mercado(datos_mercado)
        spread_dict = json.loads(spread)
        return spread_dict
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500

#Ruta para obtener los spreads de todos los mercados
#Entrada: No posee
#Salida: retorna un diccionario con el spread y el market_id de cada mercado, o un mensaje de error
@bp.route('/spread', methods=['GET'])
def getMercados():
    #defino donde guardar los spreads
    spreads = []
    #obtengo todos los mercados
    mercados = obtener_mercados()
    if mercados:
        #obtengo todos los id de los mercados (market_id)
        ids = obtener_idMercados(mercados)
        i = 0
        #recorro la lista de id de mercados, calculo el spread en cada mercado y lo almaceno como diccionario
        while i < len(ids):
            #obtengo el un mercado en específico según la iteración
            datos_mercado = obtener_datos_mercado(ids[i])
            #defino donde guardar el spread del mercado en específico
            spread = []
            if datos_mercado:
                #obtengo el spread del mercado
                spread = obtener_spread_mercado(datos_mercado)
                #convierto el spread en un diccionario
                spread_dict = json.loads(spread) 
                #agrego el spread a la lista de spreads
                spreads.append(spread_dict) 
                i=i+1
            #en caso de no tener los datos del mercado retorno un error
            else:
                return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500
        #retorno los spreads
        return jsonify(spreads)
    #en caso de no obtener los datos de lo mercados retorno un error
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API externa'}), 500


#Ruta para crear o actualizar un spread alerta de un mercado especifico
#Entrada: recibe como request un JSON con el market_id y el spread
#Salida: retorna el mensaje de creacion o actualización del spread de alerta
@bp.route('/spread/alerta', methods=['POST'])
def guardar_spread():
    #uso los spreads de alerta para almacenar el spread
    global spreads_alerta
    #obtengo los datos del JSON ingresado
    data = request.json
    market_id = data.get('market_id')
    spread_nuevo = data.get('spread')
    #si el JSON no contiene los datos se retorna un mensaje de error
    if market_id is None or spread_nuevo is None:
        return jsonify({'error': 'El JSON enviado no contiene market_id o spread'}), 400
    #en caso contrario, se almacena el spread y se identifica si fue una actualizacion o un nuevo spread
    else:
        if guardar_spread_alerta(spreads_alerta, market_id, spread_nuevo):
            return jsonify({'mensaje': 'Spread de alerta actualizado correctamente'}), 200
        else:
            return jsonify({'mensaje': 'Spread de alerta guardado correctamente'}), 200

#Ruta para realizar la comparacion del spread de alerta con el spread actual del mercado
#Entrada: recibe como un string el 'mercado', el cual es el market_id del mercado
#Salida: retorna el mensaje de la comparacion entre el spread de alerta y el actual
@bp.route('/spread/alerta/<mercado>', methods=['GET'])
def consultar_spread_alerta(mercado):
    #se obtienen los spreads de alerta almacenados
    global spreads_alerta
    #en caso de que no existan se retorna un mensaje
    if not spreads_alerta:
         return jsonify({'mensaje': 'No se han establecido spreads de alerta'}), 404
    #se convierte el market_id en mayúscula     
    mercadoUpper = mercado.upper()
    #buscar existencia de spread     
    existe_spread = encontrar_spread(spreads_alerta, mercadoUpper)
    #en el caso de encontrar un spread guardado como alerta para ese mercado se obtiene el spread actual del mercado
    if existe_spread[0]:
           spread_guardado = existe_spread[1]
           spread_actual = spread_mercado(mercadoUpper)
           valor_spread_actual = spread_actual['spread']
           #se realizan las comparaciones entre el spread guardado como alerta y el spread actual, para luego retornar el mensaje correspondiente junto a los spreads y el market_id
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
    #en caso de no encontrar un spread guardado como alerta para este mercado se retorna un mensaje
    else:

        return jsonify({'mensaje': 'No hay spread guardado para este mercado'}), 404
    


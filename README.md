# Desafio Buda Spread API

## Descripción general:

- El propósito general de la API es obtener los spreads de los mercados de Buda.com, tomando en cuenta que un spread es la diferencia entre
  la orden de venta más barata y la orden de compra más cara del mercado.

- La api puede obtener el spread de un mercado específico, consultar el spread de todos los mercados a la vez y también generar un spread de alerta,
  el cual se puede consultar para identificar como se diferencia el spread actual del mercado con el spread de alerta guardado.

## Autor:

- Diego Gajardo (diego.gajardo.s@usach.cl)

## Entorno:

- Python 3
- Flask
- Docker

## Estructura:

- carpeta src: contiene todo el código del proyecto
- archivo api.py: realiza las consultas a la api de buda.com
- archivo data_processing.py: realiza el procesamiento de datos obtenidos
- archivo routes.py: ejecuta las peticiones http del usuario devolviendo los resultados como JSON
- archivo globals.py: contiene una lista donde almacenar el spread a guardar
- archivo test_run.py: archivo de copia de run.py utilizado para la ejecución de los test
- carpeta tests: contiene los tests de cada modulo
- archivo test_api.py: contiene los tests de las funcionalidades del archivo api.py
- archivo test_data_processing.py: contiene los tests de las funcionalidades del archivo data_processing.py
- archivo test_routes.py: contiene los tests de las funcionalidades del archivo routes.py
- los archivos __init__.py son para indicar a Python que el directorio funcione como un paquete

## Endpoints:


### Spread mercado específico:

- localhost:<<puerto>>/spread/<<mercado>> | método: GET

#### Parámetros de solicitud: 

- <<puerto>> corresponde al puerto otorgado en la ejecución de la imagen docker
- <<mercado>> corresponde al market_id del mercado

#### Respuestas esperadas: 

- si el mercado existe, como por ejemplo BTC-CLP, se espera una respuesta JSON del tipo: {"market_id": "BTC-CLP", "spread": 345748.8500000015}
- si el mercado no se encuentra, se espera una respuesta JSON del tipo: {"error": "No se pudieron obtener los datos de la API externa"}

#### Ejemplos de uso:

- mercado existente: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/BTC-CLP

- mercado no existente: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/X

### Spread todos los mercados:

- localhost:<<puerto>>/spread | método: GET

#### Parámetros de solicitud: 

- no requiere parámetros

#### Respuestas esperadas:

- retorna un una lista de JSON con los spreads de cada mercado
[
  {
    "market_id": "BTC-CLP",
    "spread": 323147.0
  },
  {
    "market_id": "BTC-COP",
    "spread": 4993074.730000019
  }
  ...]

#### Ejemplos de uso:

- ruta a consumir, usando puerto 5000: http://localhost:5000/spread

### Guardar spread de alerta:

- localhost:<<puerto>>/spread/alerta | método: POST | 

#### Parámetros de solicitud:

- <puerto> corresponde al puerto otorgado en la ejecución de la imagen docker
- JSON de formato: { "market_id": "<<market_id>>","spread": <<numero>>}
	siendo <<market_id>> el id del mercado del cual se quiere registrar o actualizar una alerta
	y <numero> el valor del spread que se desea registrar
	
#### Respuestas esperadas:

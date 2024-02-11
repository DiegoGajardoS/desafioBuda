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


## Rutas disponibles:

- consultar spread mercado 'X' : http://localhost:puerto/spread/X
- consultar spread de todos los mercados: http://localhost:puerto/spread
- crear spread de alerta: http://localhost:puerto/spread/alerta
- consultar spreade de alerta de mercado 'X' http://localhost:puerto/spread/alerta/X


## Endpoints:

### Spread mercado específico:

- localhost:puerto/spread/mercado | método: GET

#### Parámetros de solicitud: 

- puerto corresponde al puerto otorgado en la ejecución de la imagen docker
- mercado corresponde al market_id del mercado

#### Respuestas esperadas: 

- si el mercado existe, como por ejemplo BTC-CLP, se espera una respuesta JSON del tipo: {"market_id": "BTC-CLP", "spread": 345748.8500000015}
- si el mercado no se encuentra, se espera una respuesta JSON del tipo: {"error": "No se pudieron obtener los datos de la API externa"}

#### Ejemplos de uso:

- mercado existente: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/BTC-CLP

- mercado no existente: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/X



### Spread todos los mercados:

- localhost:puerto/spread | método: GET

#### Parámetros de solicitud: 

- puerto corresponde al puerto otorgado en la ejecución de la imagen docker

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

- localhost:puerto/spread/alerta | método: POST 

#### Parámetros de solicitud:

- puerto corresponde al puerto otorgado en la ejecución de la imagen docker
- JSON de formato: { "market_id": "'market_id'","spread": 'numero'}
	siendo 'market_id' el id del mercado del cual se quiere registrar o actualizar una alerta
	y 'numero' el valor del spread que se desea registrar
	
#### Respuestas esperadas:

- en el caso de que no exista un spread de alerta previamente guardado para el mercado, se espera una respuesta JSON de tipo: 
  {"mensaje": "Spread de alerta guardado correctamente"}
- en el caso de que exista un spread de alerta previamente guardado para el mercado, se espera una respuesta JSON de tipo: 
  {"mensaje": "Spread de alerta actualizado correctamente"}
- en el caso de que el JSON enviado no contenga el market_id o un spread, se espera una respuesta JSON de tipo: 
  {"error": "El JSON enviado no contiene market_id o spread"}

#### Ejemplos de uso:

- guardar nuevo spread: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/alerta

  JSON enviado, por ejemplo mediante postman para consumir el endpoint: 
  
  { "market_id": "BTC-CLP",
    "spread": 800000 
  }

- actualizar spread: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/alerta

  asumiendo que ya existe un spread para el mercado BTC-CLP

  JSON enviado, por ejemplo mediante postman para consumir el endpoint: 

  { "market_id": "BTC-CLP",
    "spread": 900000 
  }

- JSON con error: 
  
  ruta a consumir, usando puerto 5000: http://localhost:5000/spread/alerta

  JSON enviado, por ejemplo mediante postman para consumir el endpoint: 

  { 
    "spread": 800000 
  }


### Consultar spread de alerta:

- localhost:puerto/spread/alerta/mercado | método: GET 

#### Parámetros de solicitud: 

- puerto corresponde al puerto otorgado en la ejecución de la imagen docker
- mercado corresponde al market_id del mercado

#### Respuestas esperadas: 

- en el caso de que el spread actual sea menor al spread guardado, se espera una respuesta del tipo:
  {
  "market_id": 'market_id',
  "mensaje": "El spread actual es menor al spread guardado",
  "spread actual": valor_actual,
  "spread guardado": valor guardado
  }
- en el caso de que el spread actual sea mayor al spread guardado, se espera una respuesta del tipo:
  {
  "market_id": 'market_id',
  "mensaje": "El spread actual es mayor al spread guardado",
  "spread actual": valor_actual,
  "spread guardado": valor guardado
  }
- en el caso de que el spread actual sea igual al spread guardado, se espera una respuesta del tipo:
  {
  "market_id": 'market_id',
  "mensaje": "El spread actual es igual al spread guardado",
  "spread actual": valor_actual,
  "spread guardado": valor guardado
  }
- en el caso de que no exista un spread guardado para el mercado, se espera una respuesta del tipo: 
  {
  "mensaje": "No hay spread guardado para este mercado"
  }

#### Ejemplos de uso:

- consultar spread del mercado 'BTC-CLP': 
  ruta a consumir usando el puerto 5000: http://localhost:5000/spread/alerta/BTC-CLP

- consultar spread de un mercado del que no se registra spread, por ejemplo 'UF-US'
  ruta a consumir usando el puerto 5000: http://localhost:5000/spread/alerta/UF-US


### Consideraciones:

- Al no registrar el spread de alerta en una base de datos, para poder consultar si existe una alerta en las pruebas primero se debe crear la alerta del  mercado en cada ejecución nueva de la api

## Como ejecutar: 

- primero se debe clonar la imagen docker, digitando en la consola: docker pull del1r1um/spread_api:latest
- una vez que se ha clonado la imagen docker, para ejecutar el proyecto se debe digitar en la consola el comando: docker run -it --publish puerto:5000 del1r1um/spread_api
- el valor del puerto lo indica el usuario de modo que por ejemplo al ejecutar: docker run -it --publish 8000:5000 del1r1um/spread_api, las consultas HTTP se deben realizar en ese puerto, como http://localhost:8000/spread
- para ejecutar los tests, una vez cargada la imagen se digita el comando en consola: docker run del1r1um/spread_api pytest -v


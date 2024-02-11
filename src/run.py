#Bloque de importaciones
from flask import Flask, jsonify
from app.routes import bp as api_bp

#se crea la instancia de la aplicación Flask
app = Flask(__name__)
#se registra el blueprint(api_bp) en la aplicación Flask
app.register_blueprint(api_bp)

#si este archivo es el punto de entrada principal se ejecuta la aplicación Flask en el servidor local, en el puerto 5000 con la depuración activada
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
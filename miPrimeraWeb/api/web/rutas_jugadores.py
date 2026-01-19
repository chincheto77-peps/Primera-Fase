from flask import request, Blueprint, jsonify
import controlador_jugadores
from funciones_auxiliares import Encoder

bp = Blueprint('jugadores', __name__)

@bp.route("/",methods=["GET"])
def jugadores():
    respuesta,code= controlador_jugadores.obtener_jugadores()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def jugador_por_id(id):
    respuesta,code = controlador_jugadores.obtener_jugador_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_jugador():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jugador_json = request.json
        nombre = jugador_json["nombre"]
        descripcion = jugador_json["descripcion"]
        precio=jugador_json["precio"]
        foto=jugador_json["foto"]
        ingredientes=jugador_json["ingredientes"]
        respuesta,code=controlador_jugadores.insertar_jugador(nombre, descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_jugador(id):
    respuesta,code=controlador_jugadores.eliminar_jugador(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_jugador():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jugador_json = request.json
        id = jugador_json["id"]
        nombre = jugador_json["nombre"]
        descripcion = jugador_json["descripcion"]
        precio=float(jugador_json["precio"])
        foto=jugador_json["foto"]
        ingredientes=jugador_json["ingredientes"]
        respuesta,code=controlador_jugadores.actualizar_jugador(id,nombre,descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code


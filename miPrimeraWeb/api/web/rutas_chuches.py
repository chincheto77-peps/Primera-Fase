from flask import request, Blueprint, jsonify
import controlador_chuches
from funciones_auxiliares import Encoder

bp = Blueprint('chuches', __name__)

@bp.route("/",methods=["GET"])
def chuches():
    respuesta,code= controlador_chuches.obtener_chuches()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def chuche_por_id(id):
    respuesta,code = controlador_chuches.obtener_chuche_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_chuche():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        chuche_json = request.json
        nombre = chuche_json["nombre"]
        descripcion = chuche_json["descripcion"]
        precio=chuche_json["precio"]
        foto=chuche_json["foto"]
        ingredientes=chuche_json["ingredientes"]
        respuesta,code=controlador_chuches.insertar_chuche(nombre, descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_chuche(id):
    respuesta,code=controlador_chuches.eliminar_chuche(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_chuche():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        chuche_json = request.json
        id = chuche_json["id"]
        nombre = chuche_json["nombre"]
        descripcion = chuche_json["descripcion"]
        precio=float(chuche_json["precio"])
        foto=chuche_json["foto"]
        ingredientes=chuche_json["ingredientes"]
        respuesta,code=controlador_chuches.actualizar_chuche(id,nombre,descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code


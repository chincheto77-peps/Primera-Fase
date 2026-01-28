from __future__ import print_function
from flask import request,Blueprint, jsonify
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        comentario_json = request.json
        usuario = comentario_json['usuario']
        descripcion = comentario_json['descripcion']
        respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/",methods=['GET'])
def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    return jsonify(respuesta), code




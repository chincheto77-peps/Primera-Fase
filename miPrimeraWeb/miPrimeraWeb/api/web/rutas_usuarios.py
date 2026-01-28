from __future__ import print_function
from flask import request,Blueprint, jsonify
from funciones_auxiliares import Encoder
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json['username']
        password = login_json['password']
        respuesta,code= controlador_usuarios.login_usuario(username,password)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json['username']
        password = login_json['password']
        profile = login_json['profile']
        respuesta,code= controlador_usuarios.alta_usuario(username,password,profile)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code


@bp.route("/logout",methods=['GET'])
def logout():
    respuesta,code= controlador_usuarios.logout()
    return jsonify(respuesta), code


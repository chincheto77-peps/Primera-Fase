from __future__ import print_function
from flask import request,Blueprint, jsonify
import controlador_ficheros
import os
import sys
import subprocess

bp = Blueprint('ficheros', __name__)

@bp.route ('/', methods=['POST']) 
def upload():
    try:
        contenido= request.files['fichero'] 
        nombre = request.form.get("nombre")
        respuesta,code = controlador_ficheros.guardar_fichero(nombre,contenido)
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        respuesta={"status": "ERROR"}
        code=500
    return jsonify(respuesta), code

@bp.route ('/<archivo>', methods=['GET']) 
def ver(archivo):
    try:
        respuesta,code = controlador_ficheros.ver_fichero(archivo)
    except:
        respuesta= {"status": "ERROR"}
        code=500
    return jsonify(respuesta), code

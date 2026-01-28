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
    content_type = request.headers.get('Content-Type', '')
    lc = content_type.lower()
    # aceptar JSON o form-data (multipart)
    if 'application/json' in lc:
        jugador_json = request.json
        nombre = jugador_json.get("nombre")
        descripcion = jugador_json.get("descripcion")
        valor_de_mercado = jugador_json.get("valor_de_mercado")
        filefoto = jugador_json.get("filefoto")
        estadisticas = jugador_json.get("estadisticas")
    elif 'multipart/form-data' in lc or 'application/x-www-form-urlencoded' in lc:
        # extraer campos desde form-data
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        valor_de_mercado = request.form.get('valor_de_mercado')
        estadisticas = request.form.get('estadisticas')
        # si se envía archivo, tomar su nombre; no guardamos el fichero aquí
        f = request.files.get('filefoto')
        filefoto = f.filename if f is not None else None
    else:
        respuesta={"status":"Bad request"}
        code=400
        return jsonify(respuesta), code

    # validación y conversión
    missing = []
    if not nombre:
        missing.append('nombre')
    if not descripcion:
        missing.append('descripcion')
    if valor_de_mercado is None or valor_de_mercado == '':
        missing.append('valor_de_mercado')
    if estadisticas is None:
        missing.append('estadisticas')
    if filefoto is None:
        missing.append('filefoto')
    if missing:
        respuesta = {"status": "Bad request", "missing": missing}
        code = 400
        return jsonify(respuesta), code

    try:
        valor_de_mercado = float(valor_de_mercado)
    except Exception:
        respuesta = {"status": "Bad request", "message": "valor_de_mercado debe ser numérico"}
        code = 400
        return jsonify(respuesta), code

    respuesta,code=controlador_jugadores.insertar_jugador(nombre, descripcion,valor_de_mercado,filefoto,estadisticas)
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_jugador(id):
    respuesta,code=controlador_jugadores.eliminar_jugador(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_jugador():
    content_type = request.headers.get('Content-Type')
    if content_type and 'application/json' in content_type.lower():
        jugador_json = request.json
        id = jugador_json["id"]
        nombre = jugador_json["nombre"]
        descripcion = jugador_json["descripcion"]
        valor_de_mercado=float(jugador_json["valor_de_mercado"])
        filefoto=jugador_json["filefoto"]
        estadisticas=jugador_json["estadisticas"]
        respuesta,code=controlador_jugadores.actualizar_jugador(id,nombre,descripcion,valor_de_mercado,filefoto,estadisticas)
    else:
        respuesta={"status":"Bad request"}
        code=400
    return jsonify(respuesta), code


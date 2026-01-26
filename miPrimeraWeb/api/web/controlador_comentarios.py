from bd import obtener_conexion
import sys
import datetime as dt


def convertir_comentario_a_json(comentario):
    d = {}
    d['id'] = comentario[0]
    d['usuario'] = comentario[1]
    d['descripcion'] = comentario[2]
    return d

def insertar_comentario(usuario, descripcion):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)"
            cursor.execute(query, (usuario, descripcion))
            conexion.commit()
        conexion.close()
        ret = {"status": "OK"}
        code = 200
    except Exception as e:
        ret = {"status": "ERROR", "message": str(e)}
        print("Excepción al insertar un comentario:", e, flush=True)
        code = 500
    return ret, code

def obtener_comentarios():
    comentariosjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas los comentarios", flush=True)
        code=500
    return comentariosjson,code
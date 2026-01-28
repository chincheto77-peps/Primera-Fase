from bd import obtener_conexion
import sys


def convertir_jugador_a_json(jugador):
    d = {}
    d['id'] = jugador[0]
    d['nombre'] = jugador[1]
    d['descripcion'] = jugador[2]
    d['valor_de_mercado'] = float(jugador[3])
    d['filefoto'] = jugador[4]
    d['estadisticas']=jugador[5]
    return d

def insertar_jugador(nombre, descripcion, valor_de_mercado,filefoto,estadisticas):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO jugadores(nombre, descripcion, valor_de_mercado,filefoto,estadisticas) VALUES (%s, %s, %s,%s,%s)",
                       (nombre, descripcion, valor_de_mercado,filefoto,estadisticas))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_jugadores():
    jugadoresjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, valor_de_mercado,filefoto,estadisticas FROM jugadores")
            jugadores = cursor.fetchall()
            if jugadores:
                for jugador in jugadores:
                    jugadoresjson.append(convertir_jugador_a_json(jugador))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las jugadores", flush=True)
        code=500
    return jugadoresjson,code

def obtener_jugador_por_id(id):
    jugadorjson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, valor_de_mercado,filefoto,estadisticas FROM jugadores WHERE id =" + id)
            jugador = cursor.fetchone()
            if jugador is not None:
                jugadorjson = convertir_jugador_a_json(jugador)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar un jugador", flush=True)
        code=500
    return jugadorjson,code
def eliminar_jugador(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM jugadores WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un jugador", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_jugador(id, nombre, descripcion, valor_de_mercado, filefoto,estadisticas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE jugadores SET nombre = %s, descripcion = %s, valor_de_mercado = %s, filefoto=%s, estadisticas=%s WHERE id = %s",
                       (nombre, descripcion, valor_de_mercado, filefoto,estadisticas,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualziar un jugador", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

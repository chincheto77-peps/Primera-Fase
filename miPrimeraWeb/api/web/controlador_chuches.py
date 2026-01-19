from bd import obtener_conexion
import sys


def convertir_chuche_a_json(chuche):
    d = {}
    d['id'] = chuche[0]
    d['nombre'] = chuche[1]
    d['descripcion'] = chuche[2]
    d['precio'] = float(chuche[3])
    d['foto'] = chuche[4]
    d['ingredientes']=chuche[5]
    return d

def insertar_chuche(nombre, descripcion, precio,foto,ingredientes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO chuches(nombre, descripcion, precio,foto,ingredientes) VALUES (%s, %s, %s,%s,%s)",
                       (nombre, descripcion, precio,foto,ingredientes))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_chuches():
    chuchesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM chuches")
            chuches = cursor.fetchall()
            if chuches:
                for chuche in chuches:
                    chuchesjson.append(convertir_chuche_a_json(chuche))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las chuches", flush=True)
        code=500
    return chuchesjson,code

def obtener_chuche_por_id(id):
    chuchejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM chuches WHERE id =" + id)
            chuche = cursor.fetchone()
            if chuche is not None:
                chuchejson = convertir_chuche_a_json(chuche)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una chuche", flush=True)
        code=500
    return chuchejson,code
def eliminar_chuche(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM chuches WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una chuche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_chuche(id, nombre, descripcion, precio, foto,ingredientes):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE chuches SET nombre = %s, descripcion = %s, precio = %s, foto=%s, ingredientes=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,ingredientes,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualziar una chuche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

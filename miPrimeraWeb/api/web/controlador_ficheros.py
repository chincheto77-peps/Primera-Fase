from __future__ import print_function
import os
import sys
import subprocess
from werkzeug.utils import secure_filename


def guardar_fichero(nombre,contenido):
    try:
        # sanitizar el nombre para evitar traversal y crear directorio si no existe
        nombre_seguro = secure_filename(nombre or '')
        if not nombre_seguro:
            raise ValueError('Nombre de fichero inválido')
        print(nombre_seguro, flush=True)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        print(basepath, flush=True)
        dir_archivos = os.path.join(basepath, 'static', 'archivos')
        os.makedirs(dir_archivos, exist_ok=True)
        ruta_fichero = os.path.join(dir_archivos, nombre_seguro)
        print('Archivo guardado en ' +  ruta_fichero, flush=True)
        # contenido es un FileStorage de Flask
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except:
        import traceback
        print("Excepcion al guardar el fichero", flush=True)
        traceback.print_exc()
        respuesta={"status": "ERROR"}
        code=500
    return respuesta, code

def ver_fichero(nombre):
    try:
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        ruta_fichero = os.path.join (basepath,'static/archivos',nombre) 
        salida=subprocess.getoutput("cat " + ruta_fichero)
        respuesta={"contenido": salida}
        code=200
    except:
        print("Excepcion al ver el fichero", flush=True)   
        respuesta={"contenido":""}
        code=500
    return respuesta,code    



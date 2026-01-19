from __future__ import print_function
import os
import sys
import subprocess


def guardar_fichero(nombre,contenido):
    try:
        print(nombre, flush=True)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        print(basepath, flush=True)
        ruta_fichero = os.path.join (basepath,'static/archivos',nombre) 
        print('Archivo guardado en ' +  ruta_fichero, flush=True)
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except:
        print("Excepcion al guardar el fichero", flush=True)  
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



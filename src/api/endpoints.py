# api/endpoints.py
'''
FastAPI para crear la aplicación,
Query para manejar parámetros de consulta
(query parameters), y HTTPException para 
manejar excepciones HTTP.
'''
from fastapi import FastAPI, Query, HTTPException

'''
StreamingResponse Para manejar respuestas de
tipo streaming, que son útiles para enviar
archivos grandes o generados en tiempo real.'''
from fastapi.responses import StreamingResponse

'''
la librería typing de Python se usa para
indicar que los parámetros pueden ser de un
tipo dado o None.'''
from typing import Optional

'''
json Para trabajar con datos en formato JSON.'''
import json

'''
io proporciona las herramientas necesarias
para manejar flujos de entrada/salida 
(en este caso, para manejar archivos en memoria).'''
import io

'''
zipfile: Para crear archivos ZIP en memoria.'''
import zipfile

'''
requests es una librería popular para hacer
solicitudes HTTP en Python.'''
import requests 

'''
Crear una instancia de la aplicación FastAPI para manejar
las solicitudes entrantes.'''
app = FastAPI()

# Función para obtener datos de la API externa
def get_data_from_api(endpoint: str, filters: dict) -> dict:
    try:
        base_url = "https://rickandmortyapi.com/api/"
        url = base_url + endpoint
        response = requests.get(url, params=filters)
        
        '''
        se utiliza para lanzar una excepción 
        si la respuesta HTTP indica un error.'''
        response.raise_for_status()
        
        return response.json()
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

'''
Esta ruta recibe parámetros opcionales de consulta 
(name, status, species) que se usan para filtrar datos 
de personajes de la API Rick and Morty.'''
@app.get("/fetch-data/")
def fetch_data(
    name: Optional[str] = Query(None),
    
    #Opciones: Vacío, Vivo, Muerto o desconocido
    status: Optional[str] = Query(None, pattern="^(alive|dead|unknown)?$"),
    
    species: Optional[str] = Query(None)
):
    filters = {
        "name": name,
        "status": status,
        "species": species
    }
    
    '''
    Filtra los parámetros None para que no se
    incluyan en la solicitud a la API.'''
    filters = {k: v for k, v in filters.items() if v is not None}
    
    data = get_data_from_api("character", filters) #Petición 
    return data

'''
empaqueta en un archivo ZIP y los
envía como una respuesta de descarga.'''
@app.get("/download-data/")
def download_data(
    name: Optional[str] = Query(None),
    status: Optional[str] = Query(None, pattern="^(alive|dead|unknown)$"),
    species: Optional[str] = Query(None)
):
    filters = {
        "name": name,
        "status": status,
        "species": species
    }
    
    filters = {k: v for k, v in filters.items() if v is not None}
    try:
        data = get_data_from_api("character", filters)
        
        '''
        Los datos se convierten a JSON'''
        json_data = json.dumps(data)

        '''
        Se crea un archivo ZIP en memoria'''
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("data.json", json_data)

        buffer.seek(0)#Se reinicia el puntero a su posición inicial

        '''
        El buffer de memoria se envía como respuesta utilizando
        StreamingResponse, permitiendo que el usuario descargue el
        archivo ZIP.'''
        return StreamingResponse(buffer, media_type="application/x-zip-compressed", headers={"Content-Disposition": "attachment; filename=data.zip"})
    
    except Exception as e:
        
        '''
        El buffer de memoria se envía como respuesta
        utilizando StreamingResponse, permitiendo que
        el usuario descargue el archivo ZIP.'''
        raise HTTPException(status_code=500, detail=str(e))

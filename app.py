# Esta API se encarga de poder recibir los datos generados por las estaciones avispero

from flask import Flask, request, jsonify, send_from_directory, send_file
from datetime import datetime
import os, json

app = Flask(__name__)
DATA_DIR = "jsons"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/api/datos", methods=["POST"])
def recibir_datos():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON no válido"}), 400
        
    Id = data.get("ID")
    name = data.get("Name")
    date = data.get("DATE")
    hour = data.get("UTC")
    
    filename = f"{Id}_{name}_{date}_{hour}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f)
        
    return jsonify({"status": "recibido", "archivo": filename}), 200

@app.route("/api/pending/<filename>", methods=["GET"])
def descargar_archivo(filename):
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "Archivo no encontrado"}), 404
        
    try:
        response = send_file(filepath, as_attachment=True)
        
        @response.call_on_close
        def eliminar_archivo():
            try:
                os.remove(filepath)
                print(f"Archivo {filename} eliminado tras descarga.")
            except Exception as e:
                print(f"No se pudo eliminar {filename}: {e}")
        
        return response
    except Exception as e:
        return jsonify({"error": f"No se pudo descargar el archivo: {str(e)}"}), 500


@app.route("/api/listar", methods=["GET"])
def listar_archivos():
    archivos = sorted(os.listdir(DATA_DIR))
    return jsonify(archivos)

from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os, json

app = Flask(__name__)

DATA_DIR = "jsons"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/api/datos", methods=["POST"])
def recibir_datos():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON no válido"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{timestamp}.json"
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f)

    return jsonify({"status": "recibido", "archivo": filename}), 200

@app.route("/api/pending/<filename>", methods=["GET"])
def descargar_archivo(filename):
    try:
        return send_from_directory(DATA_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404

@app.route("/api/listar", methods=["GET"])
def listar_archivos():
    archivos = sorted(os.listdir(DATA_DIR))
    return jsonify(archivos)


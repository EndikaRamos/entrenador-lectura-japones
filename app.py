from flask import Flask, render_template, request, jsonify
import whisper
import uuid
import os
import json
import random
from pykakasi import kakasi
import difflib

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATASET_FOLDER = "datasets"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lista de archivos disponibles como datasets
def get_available_datasets():
    return [f for f in os.listdir(DATASET_FOLDER) if f.endswith(".json")]

# Cargar dataset
def cargar_frases(nombre):
    try:
        path = os.path.join(DATASET_FOLDER, nombre)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Hiragana converter
kks = kakasi()
kks.setMode("J", "H")
kks.setMode("K", "H")
kks.setMode("r", "Hepburn")
conv = kks.getConverter()

def limpiar(texto):
    return texto.translate(str.maketrans("", "", "。、？！!?,. "))

@app.route("/")
def index():
    datasets = get_available_datasets()
    dataset = request.args.get("dataset", datasets[0] if datasets else "")
    frases = cargar_frases(dataset)
    frase = random.choice(frases) if frases else {}
    return render_template("index.html", frase=frase, dataset=dataset, datasets=datasets)

@app.route("/frase")
def nueva_frase():
    dataset = request.args.get("dataset", "")
    frases = cargar_frases(dataset)
    frase = random.choice(frases) if frases else {}
    return jsonify(frase)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    modelo_nombre = request.form.get("modelo", "base")
    kanji_actual = request.form.get("kanji", "")
    dataset = request.form.get("dataset", "")

    try:
        model = whisper.load_model(modelo_nombre)
    except Exception as e:
        return jsonify({"error": f"Error cargando modelo: {e}"}), 400

    audio = request.files["audio"]
    filename = f"{uuid.uuid4()}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(filepath)

    result = model.transcribe(filepath, language="ja")
    texto = result["text"].strip()
    hiragana_dicho = limpiar(conv.do(texto))

    frases = cargar_frases(dataset)
    frase_obj = next((f for f in frases if f["kanji"] == kanji_actual), None)
    hiragana_esperado = limpiar(frase_obj["hiragana"]) if frase_obj else ""

    matcher = difflib.SequenceMatcher(None, hiragana_dicho, hiragana_esperado)
    diferencias = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            diferencias.append({
                "dicho": hiragana_dicho[i1:i2],
                "esperado": hiragana_esperado[j1:j2],
                "pos": j1
            })

    return jsonify({
        "transcripcion": texto,
        "hiragana": hiragana_dicho,
        "esperado": hiragana_esperado,
        "errores": diferencias
    })

if __name__ == "__main__":
    app.run(debug=True)

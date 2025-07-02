import whisper

modelos = ["tiny", "base", "small", "medium", "large"]

print("🧠 Iniciando descarga de modelos Whisper...\n")

for modelo in modelos:
    print(f"🔽 Descargando modelo: {modelo}...")
    whisper.load_model(modelo)
    print(f"✅ Modelo {modelo} listo.\n")

print("🎉 Todos los modelos han sido descargados correctamente.")

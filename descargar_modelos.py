import whisper

for model in ["tiny", "base", "small", "medium", "large"]:
    print(f"Descargando modelo: {model}")
    whisper.load_model(model)

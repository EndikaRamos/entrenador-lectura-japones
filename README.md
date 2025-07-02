# 🧠 Entrenador de Lectura en Japonés (Marugoto A1 / N5)

Aplicación web en local para practicar la lectura y pronunciación de frases en japonés.  
Compatible con datasets por niveles (como Marugoto) y con transcripción por voz vía Whisper.

---

## ⚙️ Requisitos

- Python 3.7+
- FFmpeg
- Navegador moderno con micrófono
- Linux/macOS/WSL (funciona en local, sin cloud)

---

## 🔧 Instalación

1. Clona este repositorio y entra al directorio:

```bash
git clone https://github.com/tuusuario/entrenador-nihongo.git
cd entrenador-nihongo
```

2. Crea un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install flask git+https://github.com/openai/whisper.git
pip install pykakasi
```

> ⚠️ `difflib` ya viene con Python estándar, no necesita instalarse por separado.

4. Asegúrate de tener FFmpeg:

```bash
sudo apt-get install ffmpeg
```

---

## ⬇️ Descargar modelos Whisper (recomendado)

Ejecuta el script para descargar todos los modelos una vez:

```bash
python descargar_modelos.py
```

Esto descarga los modelos `tiny`, `base`, `small`, `medium` y `large` para usarlos localmente sin esperas.

---

## 🚀 Ejecutar la app

```bash
python app.py
```

Luego abre tu navegador en:

```
http://localhost:5000
```

---

## 📁 Estructura

```
├── app.py                # Backend Flask
├── templates/
│   └── index.html        # Interfaz web
├── static/
│   └── script.js         # Lógica frontend JS
├── datasets/             # Tus datasets por lección
│   ├── marugoto_1_3.json
│   ├── marugoto_4_6.json
│   └── marugoto_7_10.json
├── uploads/              # Audios temporales
├── descargar_modelos.py  # Script para descargar modelos Whisper
```

---

## 📚 Datasets

Los datasets son archivos `.json` dentro de la carpeta `datasets/` con esta estructura:

```json
{
  "kanji": "私は学生です。",
  "hiragana": "わたしはがくせいです。",
  "romaji": "watashi wa gakusei desu"
}
```

Puedes crear los tuyos y el sistema los reconocerá automáticamente.

---

## 💬 Créditos y agradecimientos

- OpenAI Whisper
- Kakasi para conversión de kanji a hiragana
- Marugoto (A1) como inspiración del contenido

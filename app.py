from flask import Flask, render_template, request, redirect
import os
import sqlite3
import numpy as np
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from gtts import gTTS
import difflib
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Cargar modelo ResNet50
model = ResNet50(weights='imagenet')

# Mapeo de etiquetas del modelo a nombres conocidos
DEVICE_MAP = {
    "led bulb": "Bombilla LED",
    "incandescent bulb": "Bombilla incandescente",
    "refrigerator": "Frigorífico (A++)",
    "fridge": "Frigorífico (A++)",
    "television": "Televisor LED (32\")",
    "tv": "Televisor LED (32\")",
    "laptop": "Ordenador portátil",
    "desktop computer": "Ordenador de sobremesa",
    "microwave": "Microondas",
    "washing machine": "Lavadora",
    "dishwasher": "Lavavajillas",
    "air conditioner": "Aire acondicionado (frío)",
    "heater": "Estufa eléctrica",
    "electric heater": "Estufa eléctrica",
    "game console": "Consola de videojuegos",
    "phone charger": "Cargador de móvil",
    "router": "Router Wi-Fi",
    "hair dryer": "Secador de pelo",
    "electric oven": "Horno eléctrico",
    "iron": "Plancha",
    "coffee maker": "Cafetera eléctrica",
    "vacuum cleaner": "Aspiradora",
    "printer": "Impresora",
    "monitor": "Monitor de PC (24\")"
}

# Eliminar audios antiguos
def limpiar_audios():
    for fname in os.listdir("static"):
        if fname.startswith("audio_") and fname.endswith(".mp3"):
            try:
                os.remove(os.path.join("static", fname))
            except Exception as e:
                print(f"No se pudo borrar {fname}: {e}")

# Obtener información del dispositivo desde la base de datos
def get_device_info(nombre):
    try:
        with sqlite3.connect("electrodomesticos.db") as con:
            cur = con.cursor()
            cur.execute("SELECT potencia_w FROM electrodomesticos WHERE LOWER(nombre) = ?", (nombre.lower(),))
            row = cur.fetchone()
            return float(row[0]) if row else None
    except sqlite3.Error as e:
        print("Error en la base de datos:", e)
        return None

# Clasificación del nivel de uso energético
def get_usage_level(kwh):
    if kwh < 1:
        return "Bajo", ["Sigue usándolo eficientemente", "Apágalo cuando no lo uses"]
    elif kwh < 3:
        return "Moderado", ["Úsalo en horarios valle", "Asegúrate de que tenga eficiencia energética"]
    else:
        return "Alto", ["Reduce el tiempo de uso", "Considera cambiarlo por uno más eficiente"]

# Generar archivo de voz con gTTS
def speak_text(text):
    limpiar_audios()
    audio_name = f"audio_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join("static", audio_name)
    tts = gTTS(text=text, lang='es')
    tts.save(audio_path)
    return audio_name

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_energy():
    name = request.form["device_name"]
    hours = float(request.form["usage_hours"])
    watts = get_device_info(name)
    if watts is None:
        watts = 100  # Valor por defecto

    kwh = (watts * hours) / 1000
    level, advice = get_usage_level(kwh)

    speech_text = f"Has seleccionado {name}. Se ha usado durante {hours} horas. Consumo estimado {round(kwh, 2)} kilovatios hora. Nivel de consumo {level}."
    audio_name = speak_text(speech_text)

    result = {
        "device": name,
        "hours": hours,
        "watts": watts,
        "kwh": round(kwh, 2),
        "level": level,
        "advice": advice,
        "audio_file": audio_name
    }

    return render_template("index.html", result=result, uuid=uuid.uuid4().hex)

@app.route("/recognize", methods=["POST"])
def recognize_image():
    img_file = request.files.get("device_image")
    if not img_file:
        return redirect("/")

    filename = img_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img_file.save(filepath)

    # Procesar la imagen
    img = image.load_img(filepath, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    decoded = decode_predictions(preds, top=5)[0]

    recognized_label = None
    for _, label, prob in decoded:
        label_clean = label.replace("_", " ").lower()

        if label_clean in DEVICE_MAP:
            recognized_label = DEVICE_MAP[label_clean]
            break

        closest = difflib.get_close_matches(label_clean, DEVICE_MAP.keys(), n=1, cutoff=0.5)
        if closest:
            recognized_label = DEVICE_MAP[closest[0]]
            break

    if not recognized_label:
        recognized_label = "dispositivo desconocido"

    usage_hours = 2
    watts = get_device_info(recognized_label)
    if watts is None:
        watts = 100

    kwh = (watts * usage_hours) / 1000
    level, advice = get_usage_level(kwh)

    speech_text = f"Imagen reconocida como {recognized_label}. Se estima un uso de {usage_hours} horas. Consumo aproximado de {round(kwh, 2)} kilovatios hora. Nivel de consumo {level}."
    audio_name = speak_text(speech_text)

    result = {
        "device": recognized_label,
        "hours": usage_hours,
        "watts": watts,
        "kwh": round(kwh, 2),
        "level": level,
        "advice": advice,
        "predictions": decoded,
        "audio_file": audio_name
    }

    return render_template("index.html", result=result, uuid=uuid.uuid4().hex)
os.makedirs("static", exist_ok=True)
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
    app.run(debug=True)







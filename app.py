from flask import Flask, render_template, request, redirect
import os
import sqlite3
import numpy as np
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from gtts import gTTS
from playsound import playsound
import difflib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

MODEL_PATH = "resnet50_imagenet_tf.2.0.h5"
model = ResNet50(weights=None)
model.load_weights(MODEL_PATH)

# Mapeo de etiquetas a nombres de la base de datos
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



# Obtener información de la base de datos
def get_device_info(nombre):
    con = sqlite3.connect("electrodomesticos.db")
    cur = con.cursor()
    cur.execute("SELECT potencia_w FROM electrodomesticos WHERE LOWER(nombre) = ?", (nombre.lower(),))
    row = cur.fetchone()
    con.close()
    if row:
        return float(row[0])
    return None

def get_usage_level(kwh):
    if kwh < 1:
        return "Bajo", ["Sigue usándolo eficientemente", "Apágalo cuando no lo uses"]
    elif kwh < 3:
        return "Moderado", ["Úsalo en horarios valle", "Asegúrate de que tenga eficiencia energética"]
    else:
        return "Alto", ["Reduce el tiempo de uso", "Considera cambiarlo por uno más eficiente"]

#  función para hablar usando gTTS
def speak_text(text):
    tts = gTTS(text=text, lang='es')
    audio_path = os.path.join("static", "audio.mp3")
    tts.save(audio_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_energy():
    name = request.form["device_name"]
    hours = float(request.form["usage_hours"])
    watts = get_device_info(name)
    if watts is None:
        watts = 100  

    kwh = (watts * hours) / 1000
    level, advice = get_usage_level(kwh)

    # Leer en voz alta
    speech_text = f"Has seleccionado {name}. Se ha usado durante {hours} horas. Consumo estimado {round(kwh, 2)} kilovatios hora. Nivel de consumo {level}."
    speak_text(speech_text)

    return render_template("index.html", result={
        "device": name,
        "hours": hours,
        "watts": watts,
        "kwh": round(kwh, 2),
        "level": level,
        "advice": advice
    })

@app.route("/recognize", methods=["POST"])
def recognize_image():
    img_file = request.files.get("device_image")
    if not img_file:
        return redirect("/")

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], img_file.filename)
    img_file.save(filepath)

    img = image.load_img(filepath, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    decoded = decode_predictions(preds, top=3)[0]

    recognized_label = None

    for _, label, prob in decoded:
        label_clean = label.replace("_", " ").lower()

        if label_clean in DEVICE_MAP:
            recognized_label = DEVICE_MAP[label_clean]
            break

        closest = difflib.get_close_matches(label_clean, DEVICE_MAP.keys(), n=1, cutoff=0.6)
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

    return render_template("index.html", result={
        "device": recognized_label,
        "hours": usage_hours,
        "watts": watts,
        "kwh": round(kwh, 2),
        "level": level,
        "advice": advice,
        "predictions": decoded
    })

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)




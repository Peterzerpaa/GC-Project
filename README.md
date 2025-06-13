# GC-Project

**GC-Project** is a web application designed to help address climate-related issues by analyzing household energy consumption. It combines technologies such as image recognition using AI, voice transcription, and energy usage calculation based on a real database.

---

## Features

- Energy consumption calculator for household appliances using a SQL database.
- Image recognition powered by a pre-trained AI model (ResNet50).
- Voice transcription for spoken input.
- Explanation of the energy consumption level and personalized advice to improve it.

---

## Technologies Used

### Backend:
- Python
- Flask
- SQLite3
- Keras + TensorFlow (ResNet50)
- OpenCV (`cv2`)
- `speech_recognition`
- `gTTS` (Google Text-to-Speech)

### Frontend:
- HTML5
- CSS3

### Additional:
- Python virtual environment (`venv`)

---

## Project Structure
GC-Project/
│
├── app.py # Main Flask application
├── templates/
│ └── index.html # HTML interface
├── static/
│ └── style.css # CSS styles
├── uploads/ # Folder for uploaded images (ignored by Git)
├── electrodomesticos.db # SQLite database of appliances
├── .gitignore # Git ignore file
└── README.md # Project documentation


---

## Large Files Not Included

To keep the repository lightweight, the following large files are **not included** and must be downloaded or generated manually:

- `resnet50_imagenet_tf.2.0.h5`  
  Pre-trained ResNet50 weights from Keras.  
  Download it from [here](https://github.com/fchollet/deep-learning-models/releases) or generate it with:

  ```python
  from keras.applications.resnet50 import ResNet50
  model = ResNet50(weights='imagenet')
  model.save_weights("resnet50_imagenet_tf.2.0.h5")
.venv/
Python virtual environment. It is excluded from Git due to size. Create it locally with:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


Installation
Install the required packages with:

bash
Copiar
Editar
pip install -r requirements.txt
Example requirements.txt content:

nginx
Copiar
Editar
Flask
tensorflow
keras
numpy
Pillow
gtts
speechrecognition
opencv-python
How to Run
Activate the virtual environment:

bash
Copiar
Editar
source .venv/bin/activate
Start the Flask app:

bash
Copiar
Editar
python app.py
Open your browser and go to:
http://127.0.0.1:5000/


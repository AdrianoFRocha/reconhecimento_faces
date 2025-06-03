from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
import datetime

app = Flask(__name__)

# Carregar imagens conhecidas
known_faces = []
known_names = []
path = "imagens_conhecidas/"

for file_name in os.listdir(path):
    img = face_recognition.load_image_file(os.path.join(path, file_name))
    encoding = face_recognition.face_encodings(img)[0]
    known_faces.append(encoding)
    known_names.append(os.path.splitext(file_name)[0])

# Inicializar captura de vídeo
video_capture = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Redimensionar para processamento
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detectar rostos
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, encoding)
            name = "Desconhecido"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Registrar presença
            with open("presenca.csv", "a") as file:
                file.write(f"{name}, {datetime.datetime.now()}\n")

            # Desenhar identificação na imagem
            top, right, bottom, left = location
            cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)
            cv2.putText(frame, name, (left*4, top*4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtém a porta do ambiente ou usa 5000 como padrão
    app.run(host="0.0.0.0", port=port, debug=True)

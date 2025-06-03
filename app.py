import cv2
import mediapipe as mp
import datetime
from flask import Flask, render_template, Response

app = Flask(__name__)

# Inicializar o módulo de detecção facial do Mediapipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Captura de vídeo
video_capture = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Converter para RGB (necessário para Mediapipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar rostos
        results = face_detection.process(rgb_frame)
        
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                
                # Desenhar um quadrado em torno do rosto
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Registrar presença
                with open("presenca.csv", "a") as file:
                    file.write(f"Rosto detectado, {datetime.datetime.now()}\n")

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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)





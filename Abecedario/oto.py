import cv2
import mediapipe as mp
import numpy as np
from math import degrees, acos
from flask import Flask, render_template, Response
from PIL import ImageFont, ImageDraw, Image

app = Flask(__name__)

# Función para obtener los ángulos de las articulaciones de los dedos
def obtenerAngulos(results, width, height):
    angulos_dedos = []
    for hand_landmarks in results.multi_hand_landmarks:
        coords = {
            "pinky": [(mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, mp_hands.HandLandmark.PINKY_MCP)],
            "ring": [(mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_MCP)],
            "middle": [(mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP)],
            "index": [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.INDEX_FINGER_MCP)],
            "thumb_outer": [(mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.THUMB_MCP)],
            "thumb_inner": [(mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_MCP, mp_hands.HandLandmark.WRIST)]
        }
        
        for key, value in coords.items():
            x1, y1 = [int(hand_landmarks.landmark[value[0][0]].x * width), int(hand_landmarks.landmark[value[0][0]].y * height)]
            x2, y2 = [int(hand_landmarks.landmark[value[0][1]].x * width), int(hand_landmarks.landmark[value[0][1]].y * height)]
            x3, y3 = [int(hand_landmarks.landmark[value[0][2]].x * width), int(hand_landmarks.landmark[value[0][2]].y * height)]
            
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            p3 = np.array([x3, y3])

            l1 = np.linalg.norm(p2 - p3)
            l2 = np.linalg.norm(p1 - p3)
            l3 = np.linalg.norm(p1 - p2)

            num_den = (l1**2 + l3**2 - l2**2) / (2 * l1 * l3)
            num_den = np.clip(num_den, -1.0, 1.0)
            angulo = degrees(acos(num_den))
            angulos_dedos.append(angulo)

    return angulos_dedos

# Función para determinar las letras en función de los ángulos de los dedos
def condicionalesLetras(dedos, frame):
    try:
        font = ImageFont.truetype("DINRoundPro.ttf", 50)  # Ajusta el tamaño de la fuente aquí
    except IOError:
        font = ImageFont.load_default()

    letras = {
        "Letra - E": [0, 0, 0, 0, 0, 0],
        "Letra - A": [1, 1, 0, 0, 0, 0],
        "Letra - I": [0, 0, 1, 0, 0, 0],
        "Letra - O": [1, 0, 1, 0, 0, 0],
        "Letra - U": [0, 0, 1, 0, 0, 1],
        "Letra - B": [0, 0, 1, 1, 1, 1],
        "Letra - D": [0, 0, 0, 0, 0, 1],
        "Letra - K": [1, 1, 0, 0, 1, 1],

        "Letra - L": [1, 1, 0, 0, 0, 1],
        "Letra - C": [1, 1, 1, 1, 1, 1],
        "Letra - W": [0, 1, 0, 1, 1, 1],
        "Letra - N": [0, 1, 0, 0, 1, 1],
        "Letra - Y": [1, 1, 1, 0, 0, 0],
        "Letra - F": [1, 1, 1, 1, 1, 0],
        "Letra - P": [0, 1, 1, 1, 1, 1],
        "Letra - V": [0, 1, 0, 0, 1, 1],

    }

    correct_color = (0, 255, 0)  # Verde
    incorrect_color = (250, 128, 114)  # Rojo
    color = incorrect_color
    letra_detectada = 'Idenficado'

    for letra, config in letras.items():
        if dedos == config:
            color = correct_color
            letra_detectada = letra
            print(letra)
            break

    height, width, _ = frame.shape
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)

    # Dibujar el rectángulo central inferior
    rect_width = 500
    rect_height = 100
    rect_start = (int((width - rect_width) / 2), height - rect_height)
    rect_end = (int((width + rect_width) / 2), height)
    draw.rectangle([rect_start, rect_end], fill=color, outline=(255, 255, 255), width=5)

    # Dibujar borde alrededor del texto
    text_bbox = draw.textbbox((0, 0), letra_detectada, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = (int((width - text_width) / 2), height - rect_height + int((rect_height - text_height) / 2))
    border_color = (255, 255, 255)  # blanco
    offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for offset in offsets:
        draw.text((text_position[0] + offset[0], text_position[1] + offset[1]), letra_detectada, font=font, fill=border_color)

    # Dibujar texto
    draw.text(text_position, letra_detectada, font=font, fill=(255, 255, 255, 255))

    frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
    return frame


# Inicialización de MediaPipe y OpenCV
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
wCam, hCam = 1280, 720
cap.set(3, wCam)
cap.set(4, hCam)

# Mueve la variable lectura_actual fuera de la función para mantener su valor entre llamadas
lectura_actual = 0

def generate():
    global lectura_actual  # Declara la variable como global
    try:
        font = ImageFont.truetype("DINRoundPro.ttf", 50)
    except IOError:
        font = ImageFont.load_default()
        
    rect_start = None
    rect_end = None
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.75) as hands, mp_pose.Pose(min_detection_confidence=0.75) as pose, mp_face_mesh.FaceMesh(min_detection_confidence=0.75) as face_mesh:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            pose_results = pose.process(frame_rgb)
            face_mesh_results = face_mesh.process(frame_rgb)

            if results.multi_hand_landmarks:
                angulosid = obtenerAngulos(results, width, height)
                dedos = []
                if angulosid[5] > 125:
                    dedos.append(1)
                else:
                    dedos.append(0)

                if angulosid[4] > 150:
                    dedos.append(1)
                else:
                    dedos.append(0)

                for id in range(4):
                    if angulosid[id] > 90:
                        dedos.append(1)
                    else:
                        dedos.append(0)
                        
                pinky = angulosid[0:2]
                pinkY = sum(pinky)
                resta = pinkY - lectura_actual
                lectura_actual = pinkY

                if dedos == [0, 1, 0, 0, 1, 0] and abs(resta) > 30:
                    font = ImageFont.truetype("DINRoundPro.ttf", 50)
                    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    draw = ImageDraw.Draw(frame_pil)
                    
                    # Cuadro inferior central
                    rect_start = (int(width / 2) - 50, height - 100)
                    rect_end = (int(width / 2) + 50, height)
                    draw.rectangle([rect_start, rect_end], fill=(255, 255, 255))
                    
                    text_position = (int(width / 2) - 25, height - 90)
                    draw.text(text_position, 'J', font=font, fill=(0, 0, 0, 255))
                    frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
                    print("J en movimiento")

                frame = condicionalesLetras(dedos, frame)

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    pose_results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1, circle_radius=1))

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)



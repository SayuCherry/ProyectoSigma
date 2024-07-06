from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

# Definir las posiciones de las manos para cada letra del alfabeto
# Esto es solo un ejemplo básico, deberás ajustar estos puntos basándote en la imagen proporcionada
alphabet_positions = {
    "A": [1, 1, 1, 1, 1],
    "B": [1, 1, 1, 1, 0],
    "C": [0, 0, 1, 0, 0],
    "D": [0, 0, 0, 1, 0],
    "E": [1, 1, 1, 1, 1],
    "F": [0, 0, 1, 1, 0],
    "G": [0, 1, 1, 0, 0],
    "H": [0, 1, 1, 0, 1],
    "I": [0, 0, 0, 0, 1],
    "J": [0, 0, 0, 0, 1], # Necesita implementación especial para movimiento
    "K": [0, 1, 1, 0, 1],
    "L": [1, 1, 0, 0, 0],
    "M": [1, 1, 1, 0, 0],
    "N": [1, 1, 1, 1, 0],
    "O": [1, 1, 1, 1, 1],
    "P": [0, 1, 1, 1, 0],
    "Q": [1, 1, 0, 1, 0],
    "R": [0, 0, 0, 1, 1],
    "S": [1, 1, 1, 1, 1],
    "T": [1, 1, 1, 1, 0],
    "U": [0, 1, 1, 0, 0],
    "V": [0, 1, 1, 0, 0],
    "W": [0, 1, 1, 1, 0],
    "X": [0, 1, 1, 1, 1],
    "Y": [1, 1, 0, 0, 1],
    "Z": [0, 0, 0, 0, 1] # Necesita implementación especial para movimiento
}

def identify_letter(fingers):
    for letter, positions in alphabet_positions.items():
        if fingers == positions:
            return letter
    return "Unknown"

def draw_rounded_rectangle(image, top_left, bottom_right, color, thickness, radius=10, alpha=0.5):
    overlay = image.copy()
    output = image.copy()

    cv2.rectangle(overlay, (top_left[0] + radius, top_left[1]), (bottom_right[0] - radius, bottom_right[1]), color, -1)
    cv2.rectangle(overlay, (top_left[0], top_left[1] + radius), (bottom_right[0], bottom_right[1] - radius), color, -1)
    cv2.circle(overlay, (top_left[0] + radius, top_left[1] + radius), radius, color, -1)
    cv2.circle(overlay, (top_left[0] + radius, bottom_right[1] - radius), radius, color, -1)
    cv2.circle(overlay, (bottom_right[0] - radius, top_left[1] + radius), radius, color, -1)
    cv2.circle(overlay, (bottom_right[0] - radius, bottom_right[1] - radius), radius, color, -1)

    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    cv2.rectangle(output, (top_left[0] + radius, top_left[1]), (bottom_right[0] - radius, bottom_right[1]), color, thickness)
    cv2.rectangle(output, (top_left[0], top_left[1] + radius), (bottom_right[0], bottom_right[1] - radius), color, thickness)
    cv2.circle(output, (top_left[0] + radius, top_left[1] + radius), radius, color, thickness)
    cv2.circle(output, (top_left[0] + radius, bottom_right[1] - radius), radius, color, thickness)
    cv2.circle(output, (bottom_right[0] - radius, top_left[1] + radius), radius, color, thickness)
    cv2.circle(output, (bottom_right[0] - radius, bottom_right[1] - radius), radius, color, thickness)

    return output

def process_hands(frame_rgb, width, height):
    hand_landmarks_list = []
    hands = mp_hands.Hands(model_complexity=1, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
    results_hands = hands.process(frame_rgb)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            landmarks = [(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in range(21)]
            fingers = [int(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y) for tip in [8, 12, 16, 20]]
            thumb = int(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
            fingers.insert(0, thumb)
            hand_landmarks_list.append((hand_landmarks, fingers))
    return hand_landmarks_list

def generate():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        hand_landmarks_list = process_hands(frame_rgb, width, height)

        for hand_landmarks, fingers in hand_landmarks_list:
            letter = identify_letter(fingers)
            text, color = f"Letra - {letter}", (0, 255, 0)

            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
            text_x, text_y = (width - text_size[0]) // 2, height - 50
            rec_x1, rec_y1 = text_x - 40, text_y - text_size[1] - 40
            rec_x2, rec_y2 = text_x + text_size[0] + 40, text_y + 40
            frame = draw_rounded_rectangle(frame, (rec_x1, rec_y1), (rec_x2, rec_y2), color, 2, radius=10, alpha=0.5)
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())

        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(port=5001, debug=False)

cap.release()

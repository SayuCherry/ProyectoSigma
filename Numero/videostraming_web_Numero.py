from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
from PIL import ImageFont, ImageDraw, Image

app = Flask(__name__)

FACE_CONNECTIONS = frozenset([
    (10, 338), (338, 297), (297, 332), (332, 284), (284, 251), (251, 389),
    (389, 356), (356, 454), (454, 323), (323, 361), (361, 288), (288, 397),
    (397, 365), (365, 379), (379, 378), (378, 400), (400, 377), (377, 152),
    (152, 148), (148, 176), (176, 149), (149, 150), (150, 136), (136, 172),
    (172, 58), (58, 132), (132, 93), (93, 234), (234, 127), (127, 162),
    (162, 21), (21, 54), (54, 103), (103, 67), (67, 109), (109, 10)
])

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

thumb_points = [1, 2, 4]
palm_points = [0, 1, 2, 5, 9, 13, 17]
finger_base_points = [6, 10, 14, 18]
fingertips_points = [8, 12, 16, 20]

font_path = 'DINRoundPro.ttf'
font_size = 50
font = ImageFont.truetype(font_path, font_size)

def palm_centroid(coordinates_list):
    coordinates = np.array(coordinates_list)
    centroid = np.mean(coordinates, axis=0)
    return int(centroid[0]), int(centroid[1])

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

def calculate_angle(p1, p2, p3):
    p1, p2, p3 = np.array(p1), np.array(p2), np.array(p3)
    l1 = np.linalg.norm(p2 - p3)
    l2 = np.linalg.norm(p1 - p3)
    l3 = np.linalg.norm(p1 - p2)
    return np.degrees(np.arccos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))

def process_hands(frame_rgb, width, height, hands):
    hand_landmarks_list = []
    results_hands = hands.process(frame_rgb)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            coordinates_thumb = [(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in thumb_points]
            coordinates_palm = [(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in palm_points]
            coordinates_ft = [(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in fingertips_points]
            coordinates_fb = [(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in finger_base_points]
            
            thumb_finger = calculate_angle(*coordinates_thumb) > 150
            centroid = palm_centroid(coordinates_palm)
            d_centroide_ft = np.linalg.norm(np.array(centroid) - np.array(coordinates_ft), axis=1)
            d_centroide_fb = np.linalg.norm(np.array(centroid) - np.array(coordinates_fb), axis=1)
            fingers = np.append(thumb_finger, d_centroide_ft - d_centroide_fb > 0)
            hand_landmarks_list.append((hand_landmarks, fingers))
    return hand_landmarks_list

def draw_hand_tracking(frame, hand_landmarks, color=(0, 255, 0), thickness=2):
    for hand_landmark in hand_landmarks:
        x = int(hand_landmark.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
        y = int(hand_landmark.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])
        w = int((hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x - hand_landmark.landmark[mp_hands.HandLandmark.WRIST].x) * frame.shape[1])
        h = int((hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y - hand_landmark.landmark[mp_hands.HandLandmark.WRIST].y) * frame.shape[0])
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

def generate():
    with mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose, \
        mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.8) as face_mesh, \
        mp_hands.Hands(model_complexity=1, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            hand_landmarks_list = process_hands(frame_rgb, width, height, hands)
            pose_results = pose.process(frame_rgb)
            face_mesh_results = face_mesh.process(frame_rgb)
            for hand_landmarks, fingers in hand_landmarks_list:
                draw_hand_tracking(frame, [hand_landmarks], color=(255, 255, 255), thickness=2)

            drawn_texts = []
            for hand_landmarks, fingers in hand_landmarks_list:
                text, color = "Error: Mal Posicionado", (0, 0, 255)
                angle_c = calculate_angle(*[(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in [2, 3, 4]])

                if 156 < calculate_angle(*[(int(hand_landmarks.landmark[index].x * width), int(hand_landmarks.landmark[index].y * height)) for index in thumb_points]) < 170 and not fingers[1:4].any():
                    text, color = "Posicion detectada correctamente", (0, 255, 0)
                elif 120 < angle_c < 140 and not fingers[0] and fingers[1] and not fingers[2:5].any():
                    text, color = "Numero - 1", (0, 255, 0)
                elif 120 < angle_c < 140 and not fingers[0] and fingers[1:3].all() and not fingers[3:5].any():
                    text, color = "Numero - 2", (0, 255, 0)
                elif fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                    text, color = "Numero - 3", (0, 255, 0)
                elif not fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                    text, color = "Numero - 4", (0, 255, 0)
                elif fingers.all():
                    text, color = "Numero - 5", (0, 255, 0)
                elif not fingers[0] and fingers[1] and fingers[2] and fingers[3] and not fingers[4]:
                    text, color = "Numero - 6", (0, 255, 0)
                elif not fingers[0] and fingers[1] and fingers[2] and not fingers[3] and fingers[4]:
                    text, color = "Numero - 7", (0, 255, 0)
                elif not fingers[0] and fingers[1] and not fingers[2] and fingers[3] and fingers[4]:
                    text, color = "Numero - 8", (0, 255, 0)
                elif not fingers[0] and not fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                    text, color = "Numero - 9", (0, 255, 0)
                elif not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
                    text, color = "Numero - 0", (0, 255, 0)

                bbox = font.getbbox(text)
                text_x, text_y = (width - bbox[2]) // 2, height - 50 - (len(drawn_texts) * 60)
                rec_x1, rec_y1 = text_x - 20, text_y - bbox[3] - 20
                rec_x2, rec_y2 = text_x + bbox[2] + 20, text_y + 20
                drawn_texts.append(((rec_x1, rec_y1), (rec_x2, rec_y2), text, color))

            for (rec_x1, rec_y1), (rec_x2, rec_y2), text, color in drawn_texts:
                frame = draw_rounded_rectangle(frame, (rec_x1, rec_y1), (rec_x2, rec_y2), color, 2, radius=10, alpha=0.6)
                pil_img = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_img)
                draw.text((rec_x1 + 20, rec_y1 + 10), text, font=font, fill=(255, 255, 255))
                frame = np.array(pil_img)

            for hand_landmarks, fingers in hand_landmarks_list:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1), mp_drawing.DrawingSpec(color=(34, 170, 180), thickness=2))

            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks, FACE_CONNECTIONS, mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(0, 170, 255), thickness=1))

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
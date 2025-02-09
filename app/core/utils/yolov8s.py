import cv2
from ultralytics import YOLO
import base64

model = YOLO("app/model/yolov8s.pt") 
def detect_objects(name):
    # name = "man-bmw.jpg"
    img = cv2.imread(name)

    results = model.predict(source=img, conf=0.5) 

    detected_objects = {}
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0] 
        confidence = box.conf[0] 
        class_id = int(box.cls[0]) 
        label = model.names[class_id] 

        if confidence >= 0.55:
            if label not in detected_objects:
                detected_objects[label] = 1
            else:
                detected_objects[label] += 1
            # detected_objects.append(label)
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 5)
            cv2.putText(img, f"{label} {confidence:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, img_encoded = cv2.imencode('.png', img_rgb)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    return img_base64, detected_objects

# def process_folder(folder_path, outout_folder=None):
#         for filename in os.listdir(folder_path):
#             if filename.endswith((".jpg", ".jpeg", ".png")):
#                 file_path = os.path.join(folder_path, filename)
#                 processed_img = detect_objects(file_path)
#                 save_path = os.path.join(outout_folder, f"processed_{filename}")
#                 cv2.imwrite(save_path, cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR))

# folder_path = "/Users/sujanmidatani/Desktop/me/gaze_test"
# process_folder(folder_path,"output8s")

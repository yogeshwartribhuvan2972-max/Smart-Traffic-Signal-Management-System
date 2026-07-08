import cv2
from ultralytics import YOLO
import time

# ✅ Slightly better accuracy than nano (still fast)
model = YOLO("yolov8n.pt")

class VehicleCounter:
    def __init__(self, jid):

        print(f"Opening Video: videos/{jid}.mp4")

        self.cap = cv2.VideoCapture(f"videos/{jid}.mp4")

        if not self.cap.isOpened():
            print(f"FAILED -> videos/{jid}.mp4")
        print(
            jid,
            "FPS =", self.cap.get(cv2.CAP_PROP_FPS),
            "Frames =", self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        # ✅ Read real FPS to maintain original video speed
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = 1 / fps if fps > 0 else 1 / 25

        self.last_frame = None
        self.last_total = 0
        self.last_emergency = False

        # ✅ YOLO every N frames (balance speed + accuracy)
        self.skip = 2
        self.fno = 0

        # ✅ vehicle class whitelist
        self.vehicle_classes = [
            "car", "bus", "truck", "motorbike","motorcycle", "bicycle"
        ]
    
    def read(self):
        start = time.time() 

        ret, frame = self.cap.read()
        
        if not ret:
            # 🔁 loop video smoothly
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        if frame is None:
            return None, 0, False

        self.fno += 1

        # ✅ Run YOLO only every N frames
        if self.fno % self.skip == 0:

            # ✅ Lower confidence slightly → detect more vehicles (still realistic)
            results = model(frame, conf=0.30, verbose=False)
            
            total = 0
            emergency = False

            for det in results[0].boxes:
                x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
                cls = int(det.cls[0])
                label = model.names[cls]

                # ✅ Count only vehicle types
                if label in self.vehicle_classes:
                    total += 1
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        (0, 255, 0),
                        2
                    )

                # ✅ Emergency detection
                if label in ["ambulance", "fire_truck"]:
                    emergency = True
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        (0, 0, 255),
                        2
                    )

            # ✅ Snapshot result (NO accumulation here)
            self.last_total = total
            self.last_emergency = emergency
            self.last_frame = frame.copy()

        else:
            # ✅ Reuse last detected frame → smooth video
            frame = self.last_frame if self.last_frame is not None else frame
            total = self.last_total
            emergency = self.last_emergency

        # ✅ Maintain original video speed
        # elapsed = time.time() - start
        # remaining = self.delay - elapsed
        # if remaining > 0:
        #     time.sleep(remaining)

        return frame, total, emergency

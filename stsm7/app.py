from flask import Flask, Response, jsonify, render_template
import cv2, threading, time, numpy as np, webbrowser

import junctions_config
from junctions_config import JUNCTIONS
from camera import VehicleCounter
from core_logic import update_logic
state_lock = threading.Lock()
LANES = ["north", "south", "east", "west"]

app = Flask(__name__)

# -------------------- INIT CAMERAS --------------------
# -------------------- INIT CAMERAS --------------------
cameras = {
    "A_north": VehicleCounter("A_north"),
    "A_south": VehicleCounter("A_south"),
    "A_east": VehicleCounter("A_east"),
    "A_west": VehicleCounter("A_west"),

    "B_north": VehicleCounter("B_north"),
    "B_south": VehicleCounter("B_south"),
    "B_east": VehicleCounter("B_east"),
    "B_west": VehicleCounter("B_west"),

    "C_north": VehicleCounter("C_north"),
    "C_south": VehicleCounter("C_south"),
    "C_east": VehicleCounter("C_east"),
    "C_west": VehicleCounter("C_west"),
}

# -------------------- VIDEO STREAM --------------------
# -------------------- VIDEO STREAM --------------------
def gen_frames(jid, lane):
    print("STREAAM:",jid,lane)

    while True:

        frame = JUNCTIONS[jid]["frames"][lane]

        if frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

        time.sleep(0.10)
        
def make_grid_frame(jid):
    tiles = []

    frames = [JUNCTIONS[jid]["frames"].get(lane) for lane in LANES]

    for lane, frame in zip(LANES, frames):

        if frame is None:
            frame = np.zeros((432,768,3), dtype=np.uint8)

        tile = cv2.resize(frame, (384,216))

        cv2.putText(
            tile,
            lane.upper(),
            (30,45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255,255,255),
            2
        )

        tiles.append(tile)

    gap_v = np.full((216, 10, 3), 80, dtype=np.uint8)
    gap_h = np.full((10, 850, 3), 80, dtype=np.uint8)

    top = np.hstack((tiles[0], gap_v, tiles[2]))
    bottom = np.hstack((tiles[3], gap_v, tiles[1]))

    gap_h = np.full((10, top.shape[1], 3), 80, dtype=np.uint8)

    frame = np.vstack((top, gap_h, bottom))
    # top = np.hstack((tiles[0], gap_v, tiles[2]))
    # bottom = np.hstack((tiles[3], gap_v, tiles[1]))

    # frame = np.vstack((top, gap_h, bottom))

    return frame

def make_control_room_frame():

    rows = []

    for jid in ["A", "B", "C"]:

        tiles = []

        for lane in LANES:

            frame = JUNCTIONS[jid]["frames"].get(lane)

            if frame is None:
                frame = np.zeros((432,768,3), dtype=np.uint8)

            tile = cv2.resize(frame, (195,135))

            cv2.putText(
                tile,
                f"{jid}.{lane[0].upper()}",
                (6,18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                1
            )
            count = JUNCTIONS[jid]["count"][lane]
            timer = JUNCTIONS[jid]["timer"]    
            signal = JUNCTIONS[jid]["signal"][lane]
            cv2.rectangle(
                tile,
                (2, tile.shape[0]-22),
                (48, tile.shape[0]-2),
                (0,0,0),
                -1
        )
            cv2.putText(
            tile,
            f"C:{count}",
            (5, tile.shape[0]-8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0,255,255),
            1
        )
            
            cv2.rectangle(
            tile,
            (tile.shape[1]-42, tile.shape[0]-22),
            (tile.shape[1]-2, tile.shape[0]-2),
            (0,0,0),
            -1
        )
            cv2.putText(
            tile,
            f"T:{timer}",
            (tile.shape[1]-40, tile.shape[0]-8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0,255,0),
            1
        )
            if signal == "green":
                color = (0,255,0)

            elif signal == "yellow":
                color = (0,255,255)

            else:
                color = (0,0,255)

            cv2.rectangle(
                tile,
                (tile.shape[1]-28, 2),
                (tile.shape[1]-2, 24),
                (0,0,0),
                -1
            )

            cv2.circle(
                tile,
                (tile.shape[1]-12, 12),
                6,
                color,
                -1
            )
            cv2.rectangle(
                tile,
                (0,0),
                (tile.shape[1]-1, tile.shape[0]-1),
                (100,100,100),
                1
            )

            tiles.append(tile)

        gap = np.full((135,6,3), 80, dtype=np.uint8)

        row = np.hstack((
            tiles[0], gap,
            tiles[1], gap,
            tiles[2], gap,
            tiles[3]
        ))

        rows.append(row)

    gap_h = np.full((8, rows[0].shape[1], 3), 80, dtype=np.uint8)

    return np.vstack((
        rows[0],
        gap_h,
        rows[1],
        gap_h,
        rows[2]
    ))

def gen_grid_frames(jid):

    while True:

        frame = make_grid_frame(jid)

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )
        time.sleep(0.03)

def gen_control_room():

    while True:

        frame = make_control_room_frame()

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

        time.sleep(0.03)

@app.route("/video/<jid>/<lane>")
def video(jid, lane):

    return Response(
        gen_frames(jid, lane),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
@app.route("/video_grid/<jid>")
def video_grid(jid):

    return Response(
        gen_grid_frames(jid),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/video_control")
def video_control():

    return Response(
        gen_control_room(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
@app.route("/set_mode/<mode>")
def set_mode(mode):

    
    junctions_config.PENDING_MODE = mode
    # junctions_config.MODE = mode
    # print("MODE =", junctions_config.MODE)

    return jsonify({
        "status": "ok",
        "mode": mode
    })


@app.route("/manual_lane/<lane>")
def manual_lane(lane):
    
    junctions_config.MANUAL_LANE = lane
    junctions_config.MODE = "manual"
    junctions_config.PENDING_MANUAL_LANE = lane

    return jsonify({
        "status": "ok",
        "lane": lane
    })
# -------------------- STATUS API --------------------
@app.route("/status")
def status():
    return jsonify({
        jid: {
            "signal": j["signal"],
            "count": j["count"],
            "timer": j["timer"],
            "emergency": j["emergency"]
        }
        for jid, j in JUNCTIONS.items()
    })

# -------------------- HOME --------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------- MAIN LOGIC THREAD --------------------
def logic_loop():

    lanes = ["north", "south", "east", "west"]

    print("⚙ Logic Thread Started")

    for j in JUNCTIONS.values():
        j["prev_green"] = None

    while True:

        # YOLO Update
        for jid, j in JUNCTIONS.items():

            emergency = False

            if "frames" not in j:
                j["frames"] = {}

            for lane in lanes:

                frame, detected, emg = cameras[f"{jid}_{lane}"].read()

                # lane-wise count
                j["count"][lane] = detected

                # lane-wise frame
                j["frames"][lane] = frame

                if emg:
                    emergency = True

            j["emergency"] = emergency

        # Signal Logic
        update_logic()

        # Reset previous green lane
        for j in JUNCTIONS.values():

            prev = j.get("prev_green")
            curr = j.get("current_green")

            if prev is not None and prev != curr:
                #j["count"][prev] = 0
                pass

            j["prev_green"] = curr

        time.sleep(0.10)

# -------------------- AUTO OPEN BROWSER --------------------
def open_browser():
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:5000")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    threading.Thread(target=logic_loop, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(
    debug=False,
    threaded=True,
    use_reloader=False
)
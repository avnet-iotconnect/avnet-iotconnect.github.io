# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import time
import json

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "video_generic_object_detection"
UNOQ_DEMO_NAME = "video-generic-object-detection"


AUTO_MODE = True
MANUAL_TRIGGER = False
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0
CURRENT_CONFIDENCE = 0.5


def set_auto(val):
    global AUTO_MODE
    AUTO_MODE = bool(val)


def should_send():
    global IOTC_LAST_SEND, MANUAL_TRIGGER
    if AUTO_MODE:
        now = time.time()
        if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
            return False
        IOTC_LAST_SEND = now
        return True
    if MANUAL_TRIGGER:
        MANUAL_TRIGGER = False
        return True
    return False


def build_slots(detections):
    top = sorted(detections, key=lambda d: d.get("confidence", 0), reverse=True)[:4]
    slots = {}
    for i in range(4):
        if i < len(top):
            slots[f"class_name_{i+1}"] = top[i].get("class_name", "")
            slots[f"confidence_{i+1}"] = float(top[i].get("confidence", 0))
        else:
            slots[f"class_name_{i+1}"] = ""
            slots[f"confidence_{i+1}"] = 0.0
    return slots


ui = WebUI()
detection_stream = VideoObjectDetection(confidence=CURRENT_CONFIDENCE, debounce_sec=0.0)


def on_relay_command(command_name, parameters):
    global IOTC_INTERVAL_SEC, CURRENT_CONFIDENCE, MANUAL_TRIGGER
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-interval":
        try:
            if isinstance(parameters, dict):
                IOTC_INTERVAL_SEC = int(parameters.get("seconds", IOTC_INTERVAL_SEC))
            else:
                IOTC_INTERVAL_SEC = int(str(parameters).strip())
            print(f"IOTCONNECT interval set to {IOTC_INTERVAL_SEC}s")
        except Exception as e:
            print(f"IOTCONNECT interval update failed: {e}")
    elif command_name == "set-confidence":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("confidence", CURRENT_CONFIDENCE)
            else:
                val = str(parameters).strip()
            CURRENT_CONFIDENCE = max(0.0, min(1.0, float(val)))
            detection_stream.override_threshold(CURRENT_CONFIDENCE)
            print(f"IOTCONNECT confidence set to {CURRENT_CONFIDENCE}")
        except Exception as e:
            print(f"IOTCONNECT confidence update failed: {e}")
    elif command_name == "set-auto":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("enabled", True)
            else:
                val = str(parameters).strip().lower() in ("1","true","yes","on")
            set_auto(val)
            print(f"IOTCONNECT auto_mode set to {AUTO_MODE}")
        except Exception as e:
            print(f"IOTCONNECT auto_mode update failed: {e}")
    elif command_name == "run-detect":
        MANUAL_TRIGGER = True
        print("IOTCONNECT manual trigger set")


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()

ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

# Register a callback for when all objects are detected
def send_detections_to_ui(detections: dict):
    for key, value in detections.items():
        entry = {
            "content": key,
            "confidence": value.get("confidence"),
            "timestamp": datetime.now(UTC).isoformat()
        }
        ui.send_message("detection", message=entry)

    # IOTCONNECT telemetry
    if should_send():
        det_list = []
        for key, value in detections.items():
            det_list.append({"class_name": key, "confidence": float(value.get("confidence", 0))})
        confs = [d.get("confidence") for d in det_list]
        max_conf = max(confs) if confs else 0.0
        avg_conf = (sum(confs) / len(confs)) if confs else 0.0
        payload = {
            "UnoQdemo": UNOQ_DEMO_NAME,
            "auto_mode": "auto" if AUTO_MODE else "manual",
            "interval_sec": int(IOTC_INTERVAL_SEC),
            "detection_count": len(det_list),
            "max_confidence": float(max_conf),
            "avg_confidence": float(avg_conf),
            "detections_json": json.dumps(det_list),
            "status": "ok",
        }
        payload.update(build_slots(det_list))
        print("IOTCONNECT send:", payload)
        relay.send_telemetry(payload)


detection_stream.on_detect_all(send_detections_to_ui)

App.run()

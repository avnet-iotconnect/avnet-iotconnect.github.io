# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import time
import json

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "object_hunting"
UNOQ_DEMO_NAME = "object-hunting"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0
CURRENT_CONFIDENCE = 0.5

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def on_relay_command(command_name, parameters):
    global IOTC_INTERVAL_SEC, CURRENT_CONFIDENCE
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


relay.command_callback = on_relay_command

ui = WebUI()
detection_stream = VideoObjectDetection(confidence=CURRENT_CONFIDENCE)

ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))


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


def send_telemetry(detections):
    global IOTC_LAST_SEND
    now = time.time()
    if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
        return
    IOTC_LAST_SEND = now
    confs = [d.get("confidence") for d in detections if isinstance(d.get("confidence"), (int, float))]
    max_conf = max(confs) if confs else 0.0
    avg_conf = (sum(confs) / len(confs)) if confs else 0.0
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "detection_count": len(detections),
        "max_confidence": float(max_conf),
        "avg_confidence": float(avg_conf),
        "detections_json": json.dumps(detections),
        "status": "ok",
    }
    payload.update(build_slots(detections))
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def send_detections_to_ui(detections: dict):
    det_list = []
    for key, value in detections.items():
        entry = {
            "content": key,
            "timestamp": datetime.now(UTC).isoformat()
        }
        ui.send_message("detection", message=entry)
        det_list.append({"class_name": key, "confidence": float(value.get("confidence", 0))})

    send_telemetry(det_list)


detection_stream.on_detect_all(send_detections_to_ui)

App.run()

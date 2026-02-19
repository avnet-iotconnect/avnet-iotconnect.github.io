# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime, UTC
import io
import base64
import json
import shlex
import requests
from PIL.Image import Image
from PIL import Image as PILImage
from arduino.app_utils import *
from arduino.app_peripherals.usb_camera import USBCamera
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.camera_code_detection import CameraCodeDetection, Detection, draw_bounding_box
from arduino.app_bricks.dbstorage_sqlstore import SQLStore

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "code_detector"
UNOQ_DEMO_NAME = "code-detector"

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def send_telemetry(content, code_type, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "code_content": content or "",
        "code_type": code_type or "",
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


detected = False


def parse_payload(parameters):
    if isinstance(parameters, dict):
        return parameters
    if isinstance(parameters, str):
        raw = parameters.strip()
        if raw.startswith("{") and raw.endswith("}"):
            try:
                return json.loads(raw)
            except Exception:
                return {}
        tokens = shlex.split(raw)
        payload = {}
        if len(tokens) >= 1:
            payload["image_url"] = tokens[0]
        if len(tokens) >= 2:
            payload["image_type"] = tokens[1]
        if len(tokens) >= 3:
            payload["confidence"] = tokens[2]
        return payload
    return {}

def handle_detection(frame: Image, detection: Detection, force=False):
    global detected
    if detected and not force:
        return

    frame = draw_bounding_box(frame, detection)

    buffer = io.BytesIO()
    frame.save(buffer, format="JPEG", quality=100)
    b64_frame = base64.b64encode(buffer.getvalue()).decode("utf-8")

    entry = {
        "content": detection.content,
        "type": detection.type,
        "timestamp": datetime.now(UTC).isoformat(),
        "image": b64_frame,
        "image_type": "image/jpeg",
    }
    store.store("scan_log", entry)
    ui.send_message('code_detected', entry)
    detected = True

    send_telemetry(detection.content, detection.type, "ok")


def on_code_detected(frame: Image, detection: Detection):
    handle_detection(frame, detection)


def on_frame(frame: Image):
    global detected
    if detected:
        return

    buffer = io.BytesIO()
    frame.save(buffer, format="JPEG", quality=100)
    b64_frame = base64.b64encode(buffer.getvalue()).decode("utf-8")

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "image": b64_frame,
        "image_type": "image/jpeg",
    }

    ui.send_message('frame_detected', entry)


def on_list_scans():
    scans = store.read("scan_log", order_by="timestamp DESC", limit=5)
    return {"scans": scans if scans else []}


def reset_detection(_, __):
    global detected
    detected = False
    send_telemetry("", "", "reset")


def detect_codes_in_image(frame: Image):
    for method_name in ("detect_image", "detect", "process_image", "process_frame", "_detect"):
        method = getattr(detector, method_name, None)
        if callable(method):
            result = method(frame)
            if isinstance(result, Detection):
                return [result]
            if isinstance(result, list) and result:
                return [r for r in result if isinstance(r, Detection)]
    return []


def on_relay_command(command_name, parameters):
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "reset":
        reset_detection(None, None)
        return
    if command_name != "detect-code":
        return

    payload = parse_payload(parameters)
    image_data = payload.get("image")
    image_url = payload.get("image_url")

    if not image_data and not image_url:
        send_telemetry("", "", "error:no_image")
        return

    try:
        if image_url and not image_data:
            resp = requests.get(image_url, timeout=10)
            resp.raise_for_status()
            image_bytes = resp.content
        else:
            image_bytes = base64.b64decode(image_data)
        frame = PILImage.open(io.BytesIO(image_bytes))
    except Exception as e:
        send_telemetry("", "", f"error:fetch_failed:{e}")
        return

    detections = detect_codes_in_image(frame)
    if not detections:
        ui.send_message("code_not_found", {"timestamp": datetime.now(UTC).isoformat()})
        send_telemetry("", "", "not_found")
        return
    handle_detection(frame, detections[0], force=True)


def on_error(e: Exception):
    ui.send_message('error', str(e))
    send_telemetry("", "", f"error:{e}")

store = SQLStore("code-scanner.db")

camera = USBCamera(resolution=(640, 480), fps=5)
detector = CameraCodeDetection(camera)
detector.on_detect(on_code_detected)
detector.on_frame(on_frame)
detector.on_error(on_error)

ui = WebUI()
ui.expose_api('GET', '/list_scans', on_list_scans)
ui.on_message('reset_detection', reset_detection)
relay.command_callback = on_relay_command

App.run()

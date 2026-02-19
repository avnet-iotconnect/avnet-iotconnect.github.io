# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.object_detection import ObjectDetection
from PIL import Image
import io
import base64
import time
import json
import requests
import shlex
import traceback

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "object_detection"
UNOQ_DEMO_NAME = "object-detection"
DEFAULT_CONFIDENCE = 0.5
CURRENT_CONFIDENCE = DEFAULT_CONFIDENCE

object_detection = ObjectDetection()


def on_relay_command(command_name, parameters):
    global CURRENT_CONFIDENCE
    param_type = type(parameters).__name__
    print(f"IOTCONNECT command: {command_name} ({param_type}) {repr(parameters)}")
    if command_name == "set-confidence":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("confidence", CURRENT_CONFIDENCE)
            else:
                val = str(parameters).strip()
            CURRENT_CONFIDENCE = max(0.0, min(1.0, float(val)))
            print(f"IOTCONNECT confidence set to {CURRENT_CONFIDENCE}")
        except Exception as e:
            print(f"IOTCONNECT confidence update failed: {e}")
    elif command_name == "detect-objects":
        try:
            payload = parameters if parameters is not None else {}
            if isinstance(payload, str):
                raw = payload.strip()
                if raw.startswith("{") and raw.endswith("}"):
                    try:
                        payload = json.loads(raw)
                    except Exception:
                        payload = {}
                else:
                    tokens = shlex.split(raw)
                    payload = {}
                    if len(tokens) >= 1:
                        payload["image_url"] = tokens[0]
                    if len(tokens) >= 2:
                        payload["image_type"] = tokens[1]
                    if len(tokens) >= 3:
                        try:
                            payload["confidence"] = float(tokens[2])
                        except Exception:
                            payload["confidence"] = tokens[2]
            print(f"IOTCONNECT detect-objects payload: {repr(payload)}")
            on_detect_objects("iotc", payload)
        except Exception as e:
            print(f"IOTCONNECT detect-objects failed: {e}")
            print(traceback.format_exc())


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()


def send_telemetry(payload):
    payload.setdefault("UnoQdemo", UNOQ_DEMO_NAME)
    print("IOTCONNECT send:", payload)
    ok = relay.send_telemetry(payload)
    print("IOTCONNECT send result:", ok)
    return ok


def parse_data(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {}
    return data if isinstance(data, dict) else {}


def normalize_results(results):
    detections = []
    if results is None:
        return detections

    if isinstance(results, dict) and isinstance(results.get('detection'), list):
        results_list = results.get('detection')
    elif isinstance(results, list):
        results_list = results
    else:
        results_list = []

    for r in results_list:
        if not isinstance(r, dict):
            continue
        conf = r.get('confidence', r.get('score', r.get('prob', r.get('p'))))
        bbox = r.get('bbox')
        bbox_xyxy = r.get('bounding_box_xyxy')
        det = {}
        if conf is not None:
            det['confidence'] = float(conf)
        if isinstance(bbox_xyxy, (list, tuple)) and len(bbox_xyxy) >= 4:
            x1, y1, x2, y2 = bbox_xyxy[0], bbox_xyxy[1], bbox_xyxy[2], bbox_xyxy[3]
            det['x'] = x1
            det['y'] = y1
            det['w'] = max(0.0, x2 - x1)
            det['h'] = max(0.0, y2 - y1)
        elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            det['x'], det['y'], det['w'], det['h'] = bbox[0], bbox[1], bbox[2], bbox[3]
        else:
            for k in ('x', 'y', 'w', 'h'):
                if k in r:
                    det[k] = r.get(k)
        if 'class_name' in r:
            det['class_name'] = r.get('class_name')
        detections.append(det)
    return detections


def on_detect_objects(client_id, data):
    try:
        parsed = parse_data(data)
        image_data = parsed.get('image')
        image_url = parsed.get('image_url')
        confidence = parsed.get('confidence', CURRENT_CONFIDENCE)
        if not image_data and not image_url:
            ui.send_message('detection_error', {'error': 'No image data'})
            send_telemetry({
                "status": "error",
                "detection_count": 0,
                "processing_time_ms": 0,
                "has_objects": "false",
                "confidence": float(confidence) if confidence is not None else 0.0,
                "max_confidence": 0.0,
                "avg_confidence": 0.0,
                "detections_json": "[]",
                "input_type": "none",
            })
            return

        input_type = "upload"
        if image_url and not image_data:
            input_type = "url"
            try:
                resp = requests.get(image_url, timeout=10)
                resp.raise_for_status()
                image_bytes = resp.content
            except Exception as e:
                ui.send_message('detection_error', {'error': f'Failed to fetch image_url: {e}'})
                send_telemetry({
                    "status": "error",
                    "detection_count": 0,
                    "processing_time_ms": 0,
                    "has_objects": "false",
                    "confidence": float(confidence) if confidence is not None else 0.0,
                    "max_confidence": 0.0,
                    "avg_confidence": 0.0,
                    "detections_json": "[]",
                    "input_type": input_type,
                })
                return
        else:
            image_bytes = base64.b64decode(image_data)

        pil_image = Image.open(io.BytesIO(image_bytes))

        start_time = time.time() * 1000
        results = object_detection.detect(pil_image, confidence=confidence)
        print("RAW RESULTS:", results)
        diff = time.time() * 1000 - start_time

        if results is None:
            ui.send_message('detection_error', {'error': 'No results returned'})
            send_telemetry({
                "status": "error",
                "detection_count": 0,
                "processing_time_ms": int(diff),
                "has_objects": "false",
                "confidence": float(confidence) if confidence is not None else 0.0,
                "max_confidence": 0.0,
                "avg_confidence": 0.0,
                "detections_json": "[]",
                "input_type": input_type,
            })
            return

        img_with_boxes = object_detection.draw_bounding_boxes(pil_image, results)

        if img_with_boxes is not None:
            img_buffer = io.BytesIO()
            img_with_boxes.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            b64_result = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        else:
            # If drawing fails, send back the original image
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            b64_result = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        detections = normalize_results(results)
        confs = [d.get("confidence") for d in detections if isinstance(d.get("confidence"), (int, float))]
        max_conf = max(confs) if confs else 0.0
        avg_conf = (sum(confs) / len(confs)) if confs else 0.0

        # build top-4 discrete fields for dashboards
        top = sorted(detections, key=lambda d: d.get("confidence", 0), reverse=True)[:4]
        slots = {}
        for i in range(4):
            if i < len(top):
                slots[f"class_name_{i+1}"] = top[i].get("class_name", "")
                slots[f"confidence_{i+1}"] = float(top[i].get("confidence", 0))
            else:
                slots[f"class_name_{i+1}"] = ""
                slots[f"confidence_{i+1}"] = 0.0

        response = {
            'success': True,
            'result_image': b64_result,
            'detection_count': len(detections),
            'processing_time': f"{diff:.2f} ms"
        }
        ui.send_message('detection_result', response)

        send_telemetry({
            "status": "ok",
            "detection_count": len(detections),
            "processing_time_ms": int(diff),
            "has_objects": "true" if (detections and len(detections) > 0) else "false",
            "confidence": float(confidence) if confidence is not None else 0.0,
            "max_confidence": float(max_conf),
            "avg_confidence": float(avg_conf),
            "detections_json": json.dumps(detections),
            "input_type": input_type,
            **slots,
        })

    except Exception as e:
        print(f"on_detect_objects error: {e}")
        print(traceback.format_exc())
        ui.send_message('detection_error', {'error': str(e)})
        send_telemetry({
            "status": "error",
            "detection_count": 0,
            "processing_time_ms": 0,
            "has_objects": "false",
            "confidence": float(CURRENT_CONFIDENCE),
            "max_confidence": 0.0,
            "avg_confidence": 0.0,
            "detections_json": "[]",
            "input_type": "error",
        })


ui = WebUI()
ui.on_message('detect_objects', on_detect_objects)

App.run()

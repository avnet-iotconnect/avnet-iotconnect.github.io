# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.visual_anomaly_detection import VisualAnomalyDetection
from arduino.app_utils import draw_anomaly_markers
from PIL import Image
import io
import base64
import time
import os
from pathlib import Path
import json
import requests

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "concrete_crack_detector"
UNOQ_DEMO_NAME = "anomaly-detection"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0
DEFAULT_CONFIDENCE = 0.5
CURRENT_CONFIDENCE = DEFAULT_CONFIDENCE


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
            print(f"IOTCONNECT confidence set to {CURRENT_CONFIDENCE}")
        except Exception as e:
            print(f"IOTCONNECT confidence update failed: {e}")


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()


def send_telemetry(payload):
    global IOTC_LAST_SEND
    now = time.time()
    if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
        return False
    payload.setdefault("UnoQdemo", UNOQ_DEMO_NAME)
    payload["interval_sec"] = int(IOTC_INTERVAL_SEC)
    IOTC_LAST_SEND = now
    print("IOTCONNECT send:", payload)
    ok = relay.send_telemetry(payload)
    print("IOTCONNECT send result:", ok)
    return ok


anomaly_detection = VisualAnomalyDetection()

SCRIPT_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = SCRIPT_DIR / "assets"
os.makedirs(IMAGES_DIR, exist_ok=True)

def parse_data(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {}
    return data if isinstance(data, dict) else {}

def normalize_results(results):
    """
    Try to extract a list of detections with confidence and bbox.
    This is defensive because the result shape can vary by model.
    """
    detections = []
    if results is None:
        return detections

    # If wrapped in dict with detection key (current model)
    if isinstance(results, dict) and isinstance(results.get("detection"), list):
        results_list = results.get("detection")
    # If wrapped in dict with anomalies key (other models)
    elif isinstance(results, dict) and isinstance(results.get("anomalies"), list):
        results_list = results.get("anomalies")
    elif isinstance(results, list):
        results_list = results
    else:
        results_list = []

    for r in results_list:
        if not isinstance(r, dict):
            continue
        conf = r.get("confidence", r.get("score", r.get("prob", r.get("p"))))
        bbox = r.get("bbox")
        bbox_xyxy = r.get("bounding_box_xyxy")
        det = {}
        if conf is not None:
            det["confidence"] = float(conf)
        if isinstance(bbox_xyxy, (list, tuple)) and len(bbox_xyxy) >= 4:
            x1, y1, x2, y2 = bbox_xyxy[0], bbox_xyxy[1], bbox_xyxy[2], bbox_xyxy[3]
            det["x"] = x1
            det["y"] = y1
            det["w"] = max(0.0, x2 - x1)
            det["h"] = max(0.0, y2 - y1)
        elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            det["x"], det["y"], det["w"], det["h"] = bbox[0], bbox[1], bbox[2], bbox[3]
        else:
            for k in ("x", "y", "w", "h"):
                if k in r:
                    det[k] = r.get(k)
        detections.append(det)
    return detections


def on_detect_anomalies(client_id, data):
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
                "has_anomaly": "false",
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
                    "has_anomaly": "false",
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
        results = anomaly_detection.detect(pil_image)
        print("RAW RESULTS:", results)
        diff = time.time() * 1000 - start_time

        if results is None:
            ui.send_message('detection_error', {'error': 'No results returned'})
            send_telemetry({
                "status": "error",
                "detection_count": 0,
                "processing_time_ms": int(diff),
                "has_anomaly": "false",
                "confidence": float(confidence) if confidence is not None else 0.0,
                "max_confidence": 0.0,
                "avg_confidence": 0.0,
                "detections_json": "[]",
                "input_type": input_type,
            })
            return

        img_with_markers = draw_anomaly_markers(pil_image, results)

        if img_with_markers is not None:
            img_buffer = io.BytesIO()
            img_with_markers.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            b64_result = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        else:
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            b64_result = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        response = {
            'success': True,
            'result_image': b64_result,
            'detection_count': len(results.get("detection", [])) if isinstance(results, dict) else (len(results) if results else 0),
            'processing_time': f"{diff:.2f} ms"
        }
        ui.send_message('detection_result', response)

        detections = normalize_results(results)
        confs = [d.get("confidence") for d in detections if isinstance(d.get("confidence"), (int, float))]
        max_conf = max(confs) if confs else float(results.get("anomaly_max_score", 0.0)) if isinstance(results, dict) else 0.0
        avg_conf = (sum(confs) / len(confs)) if confs else float(results.get("anomaly_mean_score", 0.0)) if isinstance(results, dict) else 0.0

        send_telemetry({
            "status": "ok",
            "detection_count": len(detections),
            "processing_time_ms": int(diff),
            "has_anomaly": "true" if (detections and len(detections) > 0) else "false",
            "confidence": float(confidence) if confidence is not None else 0.0,
            "max_confidence": float(max_conf),
            "avg_confidence": float(avg_conf),
            "detections_json": json.dumps(detections),
            "input_type": input_type,
        })

    except Exception as e:
        ui.send_message('detection_error', {'error': str(e)})
        send_telemetry({
            "status": "error",
            "detection_count": 0,
            "processing_time_ms": 0,
            "has_anomaly": "false",
            "confidence": float(CURRENT_CONFIDENCE),
            "max_confidence": 0.0,
            "avg_confidence": 0.0,
            "detections_json": "[]",
            "input_type": "error",
        })


ui = WebUI()
ui.on_message('detect_anomalies', on_detect_anomalies)

App.run()

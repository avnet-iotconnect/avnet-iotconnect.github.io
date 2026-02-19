# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.audio_classification import AudioClassification
import time
import os
import io
import base64
import json

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "glass_breaking_sensor"
UNOQ_DEMO_NAME = "audio-classification"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0

# Global state
AUDIO_DIR = "/app/assets/audio"


def on_relay_command(command_name, parameters):
    global IOTC_INTERVAL_SEC
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


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()


def parse_data(data):
    if isinstance(data, str):
        return json.loads(data)
    return data if isinstance(data, dict) else {}


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


def on_run_classification(sid, data):
    try:
        parsed_data = parse_data(data)
        confidence = parsed_data.get('confidence', 0.5)
        audio_data = parsed_data.get('audio_data')
        selected_file = parsed_data.get('selected_file')

        input_audio = None
        input_type = "unknown"
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            input_audio = io.BytesIO(audio_bytes)
            input_type = "upload"
        elif selected_file:
            file_path = os.path.join(AUDIO_DIR, selected_file)
            if not os.path.exists(file_path):
                ui.send_message('classification_error', {'message': f'Sample file not found: {selected_file}'}, sid)
                send_telemetry({
                    "status": "error",
                    "input_type": "sample",
                    "selected_file": selected_file or "",
                    "class_name": "",
                    "confidence": 0,
                    "processing_time_ms": 0,
                })
                return
            with open(file_path, "rb") as f:
                input_audio = io.BytesIO(f.read())
            input_type = "sample"
        if input_audio:
            start_time = time.time() * 1000
            results = AudioClassification.classify_from_file(input_audio, confidence)
            print("RAW RESULTS:", results)
            diff = time.time() * 1000 - start_time

            response_data = { 'results': results, 'processing_time': diff }
            if results:
                response_data['classification'] = { 'class_name': results["class_name"], 'confidence': results["confidence"] }
            else:
                response_data['error'] = "No sounds detected in the audio. Try to lower the confidence threshold."

            ui.send_message('classification_complete', response_data, sid)

            # IOTCONNECT telemetry
            if results:
                send_telemetry({
                    "status": "ok",
                    "input_type": input_type,
                    "selected_file": selected_file or "",
                    "class_name": results.get("class_name", ""),
                    "confidence": float(results.get("confidence", 0)),
                    "processing_time_ms": int(diff),
                })
            else:
                send_telemetry({
                    "status": "no_detection",
                    "input_type": input_type,
                    "selected_file": selected_file or "",
                    "class_name": "",
                    "confidence": 0,
                    "processing_time_ms": int(diff),
                })
        else:
            ui.send_message('classification_error', {'message': "No audio available for classification"}, sid)
            send_telemetry({
                "status": "error",
                "input_type": input_type,
                "selected_file": selected_file or "",
                "class_name": "",
                "confidence": 0,
                "processing_time_ms": 0,
            })

    except Exception as e:
        ui.send_message('classification_error', {'message': str(e)}, sid)
        send_telemetry({
            "status": "error",
            "input_type": "unknown",
            "selected_file": "",
            "class_name": "",
            "confidence": 0,
            "processing_time_ms": 0,
        })

# Initialize WebUI
ui = WebUI()

# Handle socket messages
ui.on_message('run_classification', on_run_classification)

# Start the application
App.run()
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

import json
from datetime import datetime
from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.vibration_anomaly_detection import VibrationAnomalyDetection

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "vibration_anomaly"
UNOQ_DEMO_NAME = "vibration-anomaly-detection"

logger = Logger("vibration-detector")

vibration_detection = VibrationAnomalyDetection(anomaly_detection_threshold=1.0)

ui = WebUI()


def send_telemetry(score, detected, x, y, z, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "anomaly_score": float(score),
        "anomaly_detected": "true" if detected else "false",
        "threshold": float(vibration_detection.anomaly_detection_threshold),
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def on_override_th(value: float):
    logger.info(f"Setting new anomaly threshold: {value}")
    vibration_detection.anomaly_detection_threshold = value


# IOTCONNECT command

def on_relay_command(command_name, parameters):
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-threshold":
        try:
            val = parameters.get("threshold") if isinstance(parameters, dict) else parameters
            on_override_th(float(val))
            send_telemetry(0.0, False, 0.0, 0.0, 0.0, "threshold")
        except Exception as e:
            print(f"IOTCONNECT set-threshold failed: {e}")


relay.command_callback = on_relay_command

ui.on_message("override_th", lambda sid, threshold: on_override_th(threshold))


def get_fan_status(anomaly_detected: bool):
    return {
        "anomaly": anomaly_detected,
        "status_text": "Anomaly detected!" if anomaly_detected else "No anomaly"
    }


def on_detected_anomaly(anomaly_score: float, classification: dict):
    anomaly_payload = {
        "score": anomaly_score,
        "timestamp": datetime.now().isoformat()
    }
    ui.send_message('anomaly_detected', json.dumps(anomaly_payload))
    ui.send_message('fan_status_update', get_fan_status(True))

    send_telemetry(anomaly_score, True, 0.0, 0.0, 0.0, "anomaly")


vibration_detection.on_anomaly(on_detected_anomaly)


def record_sensor_movement(x: float, y: float, z: float):
    x_ms2 = x * 9.81
    y_ms2 = y * 9.81
    z_ms2 = z * 9.81

    ui.send_message('sample', {'x': x_ms2, 'y': y_ms2, 'z': z_ms2})

    vibration_detection.accumulate_samples((x_ms2, y_ms2, z_ms2))

    # send basic telemetry on each sample (could be throttled if needed)
    send_telemetry(0.0, False, x_ms2, y_ms2, z_ms2, "sample")


Bridge.provide("record_sensor_movement", record_sensor_movement)

App.run()

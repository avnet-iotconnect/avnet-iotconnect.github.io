# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.motion_detection import MotionDetection
import pandas as pd
from collections import deque
import time

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "real_time_accel"
UNOQ_DEMO_NAME = "real-time-accelerometer"
IOTC_INTERVAL_SEC = 2
IOTC_LAST_SEND = 0.0

# Instantiate the MotionDetection brick with a confidence threshold
CONFIDENCE = 0.4
motion_detection = MotionDetection(confidence=CONFIDENCE)

logger = Logger("real-time-accelerometer")
logger.debug(f"MotionDetection instantiated with confidence={CONFIDENCE}")

# Dataframe holding the last classification probabilities
detection_df = pd.DataFrame(
    {
        'idle': [0.0],
        'snake': [0.0],
        'updown': [0.0],
        'wave' : [0.0]
    }
)

web_ui = WebUI()

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


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

relay.command_callback = on_relay_command


def send_telemetry(classification, sample=None):
    global IOTC_LAST_SEND
    now = time.time()
    if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
        return
    IOTC_LAST_SEND = now
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "idle": float(classification.get('idle', 0.0)),
        "snake": float(classification.get('snake', 0.0)),
        "updown": float(classification.get('updown', 0.0)),
        "wave": float(classification.get('wave', 0.0)),
        "status": "ok",
    }
    if sample:
        payload["x"] = float(sample.get("x", 0))
        payload["y"] = float(sample.get("y", 0))
        payload["z"] = float(sample.get("z", 0))
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


# Expose a simple HTTP API to fetch the latest detection
def _get_detection():
    return detection_df.to_dict(orient='records')[0]

web_ui.expose_api("GET", "/detection", _get_detection)

web_ui.on_connect(
    lambda sid: (
        logger.debug(f"Client connected: {sid} - sending current detection"),
        web_ui.send_message('movement', detection_df.to_dict(orient='records')[0])
    )
)


def on_movement_detected(classification: dict):
    logger.debug(f"on_movement_detected called with: {classification}")
    if not classification:
        logger.debug("on_movement_detected received empty classification, returning")
        return

    try:
        global detection_df
        detection_df = pd.DataFrame(
            {
                'idle': [classification.get('idle', 0.0)],
                'snake': [classification.get('snake', 0.0)],
                'updown': [classification.get('updown', 0.0)],
                'wave' : [classification.get('wave', 0.0)]
            }
        )

        # Broadcast update to connected websocket client
        try:
            web_ui.send_message('movement', detection_df.to_dict(orient='records')[0])
        except Exception:
            logger.debug('Failed to emit movement websocket message')

        send_telemetry(detection_df.to_dict(orient='records')[0])

    except Exception as e:
        logger.exception(f"dataframe: Error: {e}")

# Register movement callbacks
motion_detection.on_movement_detection('idle', on_movement_detected)
motion_detection.on_movement_detection('snake', on_movement_detected)
motion_detection.on_movement_detection('updown', on_movement_detected)
motion_detection.on_movement_detection('wave', on_movement_detected)

# buffer of samples for the simple time-series chart
SAMPLES_MAX = 200
samples = deque(maxlen=SAMPLES_MAX)

# Provide a simple API to fetch recent samples for the frontend chart
def _get_samples():
    return list(samples)

web_ui.expose_api("GET", "/samples", _get_samples)


def record_sensor_movement(x: float, y: float, z: float):
    try:
        x_ms2 = x * 9.81
        y_ms2 = y * 9.81
        z_ms2 = z * 9.81

        motion_detection.accumulate_samples((x_ms2, y_ms2, z_ms2))

        sample = {
            "t": time.time(),
            "x": float(x),
            "y": float(y),
            "z": float(z)
        }

        samples.append(sample)
        try:
            web_ui.send_message('sample', sample)
        except Exception:
            logger.debug('Failed to emit sample websocket message')

        # Send sample telemetry at interval
        send_telemetry(detection_df.to_dict(orient='records')[0], sample)

    except Exception as e:
        logger.exception(f"record_sensor_movement: Error: {e}")

try:
    Bridge.provide("record_sensor_movement", record_sensor_movement)
except RuntimeError:
    pass

App.run()

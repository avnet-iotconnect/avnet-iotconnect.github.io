# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.keyword_spotting import KeywordSpotting
import threading
import time

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "keyword_spotting"
UNOQ_DEMO_NAME = "keyword-spotting"
WAIT_AFTER_DETECT_SEC = 4
WAITING_TIMER = None
LAST_DETECTED_TS = 0.0

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def send_telemetry(keyword, status="ok", state="", confidence=0.0, last_detected_ts=0.0):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "device_name": RELAY_CLIENT_ID,
        "keyword": keyword or "",
        "state": state,
        "status": status,
        "confidence": float(confidence) if confidence is not None else 0.0,
        "last_detected_ts": int(last_detected_ts) if last_detected_ts else 0,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)

def schedule_waiting():
    global WAITING_TIMER
    if WAITING_TIMER:
        WAITING_TIMER.cancel()
    WAITING_TIMER = threading.Timer(
        WAIT_AFTER_DETECT_SEC,
        lambda: send_telemetry("", "waiting", state="waiting", confidence=0.0, last_detected_ts=LAST_DETECTED_TS),
    )
    WAITING_TIMER.daemon = True
    WAITING_TIMER.start()


def on_keyword_detected():
    global LAST_DETECTED_TS
    Bridge.call("keyword_detected")
    LAST_DETECTED_TS = time.time()
    send_telemetry("hey_arduino", "detected", state="detected", confidence=1.0, last_detected_ts=LAST_DETECTED_TS)
    schedule_waiting()


spotter = KeywordSpotting()
spotter.on_detect("hey_arduino", on_keyword_detected)

App.run()

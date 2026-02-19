# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
import time

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "blink"
UNOQ_DEMO_NAME = "blink"
IOTC_INTERVAL_SEC = 1
IOTC_LAST_SEND = 0.0

led_state = False


def on_relay_command(command_name, parameters):
    global IOTC_INTERVAL_SEC, led_state
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
    elif command_name == "set-led":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("state", led_state)
            else:
                val = parameters
            led_state = bool(int(val)) if isinstance(val, (int, float, str)) else bool(val)
            Bridge.call("set_led_state", led_state)
            print(f"IOTCONNECT led_state set to {led_state}")
        except Exception as e:
            print(f"IOTCONNECT set-led failed: {e}")


relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()


def send_telemetry():
    global IOTC_LAST_SEND
    now = time.time()
    if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
        return
    IOTC_LAST_SEND = now
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "led_state": "on" if led_state else "off",
        "status": "ok",
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def loop():
    global led_state
    time.sleep(1)
    led_state = not led_state
    Bridge.call("set_led_state", led_state)
    send_telemetry()

App.run(user_loop=loop)

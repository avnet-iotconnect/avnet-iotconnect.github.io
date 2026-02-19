# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "blink_with_ui"
UNOQ_DEMO_NAME = "blink-with-ui"

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()

# Global state
led_is_on = False


def send_telemetry(state, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "led_state": "on" if state else "off",
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def get_led_status():
    return {
        "led_is_on": led_is_on,
        "status_text": "LED IS ON" if led_is_on else "LED IS OFF"
    }


def on_relay_command(command_name, parameters):
    global led_is_on
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-led":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("state", led_is_on)
            else:
                val = parameters
            led_is_on = bool(int(val)) if isinstance(val, (int, float, str)) else bool(val)
            Bridge.call("set_led_state", led_is_on)
            send_telemetry(led_is_on, "iotconnect")
        except Exception as e:
            send_telemetry(led_is_on, f"error:{e}")


relay.command_callback = on_relay_command


def toggle_led_state(client, data):
    global led_is_on
    led_is_on = not led_is_on
    Bridge.call("set_led_state", led_is_on)
    ui.send_message('led_status_update', get_led_status())
    send_telemetry(led_is_on, "ui")


def on_get_initial_state(client, data):
    ui.send_message('led_status_update', get_led_status(), client)

ui = WebUI()
ui.on_message('toggle_led', toggle_led_state)
ui.on_message('get_initial_state', on_get_initial_state)

App.run()

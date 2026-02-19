# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

# EXAMPLE_NAME = "Arduino Cloud LED Blink Example"
from arduino.app_bricks.arduino_cloud import ArduinoCloud
from arduino.app_utils import App, Bridge

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "cloud_blink"
UNOQ_DEMO_NAME = "cloud-blink"

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()

# If secrets are not provided in the class initialization, they will be read from environment variables
iot_cloud = ArduinoCloud()


def send_telemetry(led_state, source, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "led_state": "on" if led_state else "off",
        "source": source,
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def led_callback(client: object, value: bool):
    print(f"LED blink value updated from cloud: {value}")
    Bridge.call("set_led_state", value)
    send_telemetry(bool(value), "cloud", "ok")


def on_relay_command(command_name, parameters):
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-led":
        try:
            if isinstance(parameters, dict):
                val = parameters.get("state", False)
            else:
                val = parameters
            state = bool(int(val)) if isinstance(val, (int, float, str)) else bool(val)
            Bridge.call("set_led_state", state)
            send_telemetry(state, "iotconnect", "ok")
        except Exception as e:
            send_telemetry(False, "iotconnect", f"error:{e}")


relay.command_callback = on_relay_command

iot_cloud.register("led", value=False, on_write=led_callback)

App.run()

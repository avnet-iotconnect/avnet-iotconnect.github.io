# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import *

import requests
import socket
import time

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "air_quality_led_matrix"
UNOQ_DEMO_NAME = "air-quality-monitoring"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0

# Insert your API token here
API_TOKEN = "demo"

# Default city
city = "Torino"

endpoint = lambda c: f"https://api.waqi.info/feed/{c}/?token={API_TOKEN}"

AQI_LEVELS = [
    {"min": 0, "max": 50, "description": "Good"},
    {"min": 51, "max": 100, "description": "Moderate"},
    {"min": 101, "max": 150, "description": "Unhealthy for Sensitive Groups"},
    {"min": 151, "max": 200, "description": "Unhealthy"},
    {"min": 201, "max": 300, "description": "Very Unhealthy"},
    {"min": 301, "max": 500, "description": "Hazardous"},
]

# Optional: quick connectivity print (keep or remove)
try:
    s = socket.create_connection(("172.17.0.1", 8899), timeout=2)
    print("TCP to 172.17.0.1 8899: OK")
    s.close()
except Exception as e:
    print("TCP to 172.17.0.1 8899: FAIL:", e)

# ---- Command handler from IOTCONNECT (via relay server) ----
def on_relay_command(command_name: str, parameters):
    global city
    global IOTC_INTERVAL_SEC

    print("Received relay command:", command_name, parameters)

    if command_name == "set-interval":
        try:
            if isinstance(parameters, dict):
                IOTC_INTERVAL_SEC = int(parameters.get("seconds", IOTC_INTERVAL_SEC))
            else:
                IOTC_INTERVAL_SEC = int(str(parameters).strip())
            print(f"IOTCONNECT interval set to {IOTC_INTERVAL_SEC}s")
        except Exception as e:
            print(f"IOTCONNECT interval update failed: {e}")
        return

    # Example command: set-city  (parameters: {"city":"Chicago"} or "Chicago")
    if command_name == "set-city":
        new_city = None
        if isinstance(parameters, dict):
            new_city = parameters.get("city")
        elif isinstance(parameters, str):
            new_city = parameters.strip()

        if new_city:
            city = new_city
            print("City updated to:", city)
            # Send ack-ish telemetry so you can see it happened
            relay.send_telemetry({"event": "city_updated", "city": city})
        else:
            relay.send_telemetry({"event": "city_update_failed", "reason": "missing city"})

    # Example command: ping
    elif command_name == "ping":
        relay.send_telemetry({"event": "pong", "ts": int(time.time())})

    else:
        relay.send_telemetry({"event": "unknown_command", "command": command_name})

# Start relay client
relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()


def map_aqi_level(aqi_value: int) -> str:
    for level in AQI_LEVELS:
        if level["min"] <= aqi_value <= level["max"]:
            return level["description"]
    return "N/A"


def get_air_quality():
    global city
    url = endpoint(city)

    try:
        response = requests.get(url, timeout=5)
        response_json = response.json()
    except Exception as e:
        print("HTTP error:", e)
        relay.send_telemetry({"city": city, "error": "http_error", "detail": str(e)})
        return

    status = response_json.get("status")
    data = response_json.get("data")

    if status != "ok" or not data:
        print(f"API Error: {response_json}")
        relay.send_telemetry({"city": city, "error": "api_error", "raw": response_json})
        return

    aqi = data.get("aqi", -1)
    aqi_level = map_aqi_level(aqi)

    # Publish telemetry (rate-limited)
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "city": city,
        "aqi": aqi,
        "aqi_level": aqi_level
    }
    now = time.time()
    if now - IOTC_LAST_SEND >= IOTC_INTERVAL_SEC:
        print("IOTCONNECT send:", payload)
        ok = relay.send_telemetry(payload)
        print("IOTCONNECT send result:", ok)
        globals()["IOTC_LAST_SEND"] = now

    return aqi_level


Bridge.provide("get_air_quality", get_air_quality)

App.run()

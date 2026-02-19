# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_bricks.weather_forecast import WeatherForecast
from arduino.app_utils import *
import time

# ---- IOTCONNECT Relay (App Lab TCP bridge) ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "weather_forecast"
UNOQ_DEMO_NAME = "weather-forecast"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0
CITY_OVERRIDE = None

def on_relay_command(command_name, parameters):
    global IOTC_INTERVAL_SEC, CITY_OVERRIDE
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
    elif command_name == "set-city":
        try:
            if isinstance(parameters, dict):
                CITY_OVERRIDE = parameters.get("city")
            else:
                CITY_OVERRIDE = str(parameters).strip()
            print(f"IOTCONNECT city override set to: {CITY_OVERRIDE}")
        except Exception as e:
            print(f"IOTCONNECT city update failed: {e}")

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
    command_callback=on_relay_command
)
relay.start()

forecaster = WeatherForecast()


def get_weather_forecast(city: str) -> str:
    use_city = CITY_OVERRIDE or city
    forecast = forecaster.get_forecast_by_city(use_city)
    print(f"Weather forecast for {use_city}: {forecast.description}")

    # Publish telemetry (rate-limited)
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "city": use_city,
        "forecast_category": forecast.category,
        "forecast_description": forecast.description,
    }
    now = time.time()
    if now - IOTC_LAST_SEND >= IOTC_INTERVAL_SEC:
        print("IOTCONNECT send:", payload)
        ok = relay.send_telemetry(payload)
        print("IOTCONNECT send result:", ok)
        globals()["IOTC_LAST_SEND"] = now

    return forecast.category


Bridge.provide("get_weather_forecast", get_weather_forecast)

App.run()

# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

import datetime
import psutil
import time
from arduino.app_bricks.dbstorage_tsstore import TimeSeriesStore
from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "system_resources"
UNOQ_DEMO_NAME = "system-resources-logger"
IOTC_INTERVAL_SEC = 5
IOTC_LAST_SEND = 0.0

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


def send_telemetry(cpu_percent, mem_percent, ts):
    global IOTC_LAST_SEND
    now = time.time()
    if now - IOTC_LAST_SEND < IOTC_INTERVAL_SEC:
        return
    IOTC_LAST_SEND = now
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "interval_sec": int(IOTC_INTERVAL_SEC),
        "cpu_percent": float(cpu_percent),
        "mem_percent": float(mem_percent),
        "ts": int(ts),
        "status": "ok",
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


db = TimeSeriesStore()

def on_get_samples(resource: str, start: str, aggr_window: str):
    samples = db.read_samples(measure=resource, start_from=start, aggr_window=aggr_window, aggr_func="mean", limit=100)
    res = []
    for sample in samples:
        point = {
            "ts": sample[1],
            "value": sample[2],
        }
        res.append(point)
    return res

ui = WebUI()
ui.expose_api("GET", "/get_samples/{resource}/{start}/{aggr_window}", on_get_samples)

def get_events():
    ts = int(datetime.datetime.now().timestamp() * 1000)

    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    db.write_sample('cpu', cpu_percent, ts)
    ui.send_message('cpu_usage', {
        "value": cpu_percent,
        "ts": ts
    })
    # Memory usage
    mem_percent = psutil.virtual_memory().percent
    db.write_sample('mem', mem_percent, ts)
    ui.send_message('memory_usage', {
        "value": mem_percent,
        "ts": ts
    })

    send_telemetry(cpu_percent, mem_percent, ts)
    time.sleep(5)

App.run(user_loop=get_events)

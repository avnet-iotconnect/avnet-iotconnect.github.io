# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

import json, ast
from datetime import datetime, UTC
from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "unoq_pin_toggle"
UNOQ_DEMO_NAME = "unoq-pin-toggle"

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()

# ---------- Pin config: add pins here ----------
PIN_CONFIG = {
    # JDIGITAL
    "D21": {"active_low": False},
    "D20": {"active_low": False},
    "D13": {"active_low": False},
    "D12": {"active_low": False},
    "D11": {"active_low": False},
    "D10": {"active_low": False},
    "D9": {"active_low": False},
    "D8": {"active_low": False},
    "D7": {"active_low": False},
    "D6": {"active_low": False},
    "D5": {"active_low": False},
    "D4": {"active_low": False},
    "D3": {"active_low": False},
    "D2": {"active_low": False},
    "D1": {"active_low": False},
    "D0": {"active_low": False},
    # JANALOG
    "A0": {"active_low": False},
    "A1": {"active_low": False},
    "A2": {"active_low": False},
    "A3": {"active_low": False},
    "A4": {"active_low": False},
    "A5": {"active_low": False},
    # STM LEDS
    "LED3_R": {"active_low": True},
    "LED3_G": {"active_low": True},
    "LED3_B": {"active_low": True},
    "LED4_R": {"active_low": True},
    "LED4_G": {"active_low": True},
    "LED4_B": {"active_low": True},

}
PIN_NAMES = tuple(PIN_CONFIG.keys())

pin_states = {name: False for name in PIN_NAMES}

ui = WebUI()

def _iso_now() -> str:
    return datetime.now(UTC).isoformat()

def _normalize_state(value) -> bool:
    if isinstance(value, bool): return value
    if isinstance(value, (int, float)): return bool(int(value))
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("on","true","1"):  return True
        if v in ("off","false","0"): return False
    raise ValueError(f"Invalid state value: {value!r}")

def _ensure_dict(payload):
    if isinstance(payload, (list, tuple)) and len(payload) == 1:
        payload = payload[0]
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8", errors="strict")
    if isinstance(payload, str):
        s = payload.strip()
        try:
            return json.loads(s)
        except Exception:
            try:
                val = ast.literal_eval(s)
                if isinstance(val, (list, tuple)) and len(val) == 1 and isinstance(val[0], dict):
                    return val[0]
                if isinstance(val, dict):
                    return val
            except Exception:
                pass
        raise ValueError(f"Unsupported string payload: {s[:80]}...")
    raise ValueError(f"Unsupported payload type: {type(payload).__name__}")

def _state_for_hw(name: str, logical_state: bool) -> bool:
    cfg = PIN_CONFIG.get(name, {})
    return (not logical_state) if cfg.get("active_low") else logical_state


def send_telemetry(name, logical_state, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "pin_name": name,
        "pin_state": "on" if logical_state else "off",
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def on_relay_command(command_name, parameters):
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-pin":
        try:
            data = _ensure_dict(parameters)
            name = data.get("name")
            if name not in PIN_NAMES:
                raise ValueError(f"Unknown Pin '{name}'")
            logical = _normalize_state(data.get("state"))
            pin_states[name] = logical
            state_for_hw = _state_for_hw(name, logical)
            Bridge.call("set_pin_by_name", name, state_for_hw)
            send_telemetry(name, logical, "ok")
        except Exception as e:
            send_telemetry("", False, f"error:{e}")


relay.command_callback = on_relay_command


def on_pin_toggle(sid, message):
    try:
        data = _ensure_dict(message)
        name = data.get("name")
        if name not in PIN_NAMES:
            raise ValueError(f"Unknown Pin '{name}'")

        logical = _normalize_state(data.get("state"))
        pin_states[name] = logical

        state_for_hw = _state_for_hw(name, logical)
        Bridge.call("set_pin_by_name", name, state_for_hw)

        print(f"[{_iso_now()}] [{sid}] {name} -> logical={'ON' if logical else 'OFF'} hw={state_for_hw}")
        ui.send_message("pin_state_update", {
            "name": name,
            "state": logical,
            "timestamp": _iso_now()
        })

        send_telemetry(name, logical, "ok")

    except Exception as e:
        ui.send_message("error", f"Pin toggle error: {e}")
        send_telemetry("", False, f"error:{e}")


def on_get_states():
    return {"timestamp": _iso_now(), "states": pin_states}

ui.on_message("pin_toggle", on_pin_toggle)
ui.expose_api("GET", "/states", on_get_states)

App.run()

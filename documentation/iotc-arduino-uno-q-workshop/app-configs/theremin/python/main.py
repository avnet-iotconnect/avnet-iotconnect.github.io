# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.wave_generator import WaveGenerator
from arduino.app_utils import App, Logger

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "theremin"
UNOQ_DEMO_NAME = "theremin"

logger = Logger("theremin")

SAMPLE_RATE = 16000

wave_gen = WaveGenerator(
    sample_rate=SAMPLE_RATE,
    wave_type="sine",
    block_duration=0.03,
    attack=0.01,
    release=0.03,
    glide=0.02,
)

wave_gen.set_frequency(440.0)
wave_gen.set_amplitude(0.0)
_state = wave_gen.get_state()
LAST_FREQ = float(_state.get("frequency", 440.0))
LAST_AMP = float(_state.get("amplitude", 0.0))
LAST_VOLUME = int(_state.get("volume", 100))

ui = WebUI()

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def send_telemetry(freq, amp, volume, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "frequency": float(freq),
        "amplitude": float(amp),
        "volume": int(volume),
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


def on_connect(sid, data=None):
    state = wave_gen.get_state()
    ui.send_message("theremin:state", {"freq": state["frequency"], "amp": state["amplitude"]})
    ui.send_message("theremin:volume", {"volume": state["volume"]})
    send_telemetry(state["frequency"], state["amplitude"], state["volume"], "connect")


def _freq_from_x(x):
    return 20.0 * ((SAMPLE_RATE / 2.0 / 20.0) ** x)


def on_move(sid, data=None):
    global LAST_FREQ, LAST_AMP
    d = data or {}
    x = float(d.get("x", 0.0))
    y = float(d.get("y", 1.0))
    freq = d.get("freq")
    freq = float(freq) if freq is not None else _freq_from_x(x)
    amp = max(0.0, min(1.0, 1.0 - float(y)))

    wave_gen.set_frequency(freq)
    wave_gen.set_amplitude(amp)
    LAST_FREQ = float(freq)
    LAST_AMP = float(amp)

    ui.send_message("theremin:state", {"freq": freq, "amp": amp}, room=sid)
    send_telemetry(freq, amp, wave_gen.get_state()["volume"], "move")


def on_power(sid, data=None):
    global LAST_AMP
    d = data or {}
    on = bool(d.get("on", False))
    if not on:
        wave_gen.set_amplitude(0.0)
    else:
        wave_gen.set_amplitude(LAST_AMP)
    send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "power")


def on_set_volume(sid, data=None):
    global LAST_VOLUME
    d = data or {}
    volume = int(d.get("volume", 100))
    volume = max(0, min(100, volume))
    wave_gen.set_volume(volume)
    LAST_VOLUME = int(volume)
    ui.send_message("theremin:volume", {"volume": volume})
    send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "volume")


# IOTCONNECT commands

def on_relay_command(command_name, parameters):
    global LAST_FREQ, LAST_AMP, LAST_VOLUME
    print(f"IOTCONNECT command: {command_name} {parameters}")
    if command_name == "set-freq":
        try:
            val = parameters.get("freq") if isinstance(parameters, dict) else parameters
            wave_gen.set_frequency(float(val))
            LAST_FREQ = float(val)
            ui.send_message("theremin:state", {"freq": LAST_FREQ, "amp": wave_gen.get_state()["amplitude"]})
            send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "set-freq")
        except Exception as e:
            print(f"IOTCONNECT set-freq failed: {e}")
    elif command_name == "set-amp":
        try:
            val = parameters.get("amp") if isinstance(parameters, dict) else parameters
            wave_gen.set_amplitude(float(val))
            LAST_AMP = float(val)
            ui.send_message("theremin:state", {"freq": wave_gen.get_state()["frequency"], "amp": LAST_AMP})
            send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "set-amp")
        except Exception as e:
            print(f"IOTCONNECT set-amp failed: {e}")
    elif command_name == "set-volume":
        try:
            val = parameters.get("volume") if isinstance(parameters, dict) else parameters
            wave_gen.set_volume(int(val))
            LAST_VOLUME = int(val)
            ui.send_message("theremin:volume", {"volume": LAST_VOLUME})
            send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "set-volume")
        except Exception as e:
            print(f"IOTCONNECT set-volume failed: {e}")
    elif command_name == "power":
        try:
            val = parameters.get("on") if isinstance(parameters, dict) else parameters
            if isinstance(val, str):
                on = val.strip().lower() in ("1", "true", "yes", "on")
            else:
                on = bool(val)
            if not on:
                wave_gen.set_amplitude(0.0)
            else:
                wave_gen.set_amplitude(LAST_AMP)
            ui.send_message("theremin:state", {"freq": wave_gen.get_state()["frequency"], "amp": wave_gen.get_state()["amplitude"]})
            send_telemetry(wave_gen.get_state()["frequency"], wave_gen.get_state()["amplitude"], wave_gen.get_state()["volume"], "power")
        except Exception as e:
            print(f"IOTCONNECT power failed: {e}")


relay.command_callback = on_relay_command

ui.on_connect(on_connect)
ui.on_message("theremin:move", on_move)
ui.on_message("theremin:power", on_power)
ui.on_message("theremin:set_volume", on_set_volume)

App.run()

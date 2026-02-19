# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App, Bridge, FrameDesigner, Logger
from app_frame import AppFrame
import store
import threading

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "led_matrix_painter"
UNOQ_DEMO_NAME = "led-matrix-painter"

logger = Logger("led-matrix-painter")
ui = WebUI()
designer = FrameDesigner()

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def send_telemetry(action, frame=None, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "action": action,
        "frame_id": int(frame.id) if frame and frame.id is not None else 0,
        "frame_name": frame.name if frame else "",
        "frame_count": len(store.list_frames(order_by='position ASC, id ASC')) if hasattr(store, 'list_frames') else 0,
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)

store.init_db()

BRIGHTNESS_LEVELS = 8


def get_config():
    return {
        'brightness_levels': BRIGHTNESS_LEVELS,
        'width': designer.width,
        'height': designer.height,
    }


def apply_frame_to_board(frame: AppFrame):
    frame_bytes = frame.to_board_bytes()
    Bridge.call("draw", frame_bytes)


def update_board(payload: dict):
    frame = AppFrame.from_json(payload)
    apply_frame_to_board(frame)
    vector_text = frame.to_c_string()
    send_telemetry("update_board", frame)
    return {'ok': True, 'vector': vector_text}


def persist_frame(payload: dict):
    frame = AppFrame.from_json(payload)

    if frame.id is None:
        frame.id = store.save_frame(frame)
        record = store.get_frame_by_id(frame.id)
        if record:
            frame = AppFrame.from_record(record)
    else:
        store.update_frame(frame)

    apply_frame_to_board(frame)
    vector_text = frame.to_c_string()
    send_telemetry("persist_frame", frame)
    return {'ok': True, 'frame': frame.to_json(), 'vector': vector_text}


def bulk_update_frame_duration(payload) -> bool:
    duration = payload.get('duration_ms', 1000)
    store.bulk_update_frame_duration(duration)
    send_telemetry("bulk_update_duration", None)
    return True


def load_frame(payload: dict = None):
    fid = payload.get('id') if payload else None

    if fid is not None:
        record = store.get_frame_by_id(fid)
        if not record:
            return {'error': 'frame not found'}
        frame = AppFrame.from_record(record)
    else:
        frame = store.get_or_create_active_frame(brightness_levels=BRIGHTNESS_LEVELS)

    apply_frame_to_board(frame)
    vector_text = frame.to_c_string()
    send_telemetry("load_frame", frame)
    return {'ok': True, 'frame': frame.to_json(), 'vector': vector_text}


def list_frames():
    records = store.list_frames(order_by='position ASC, id ASC')
    frames = [AppFrame.from_record(r).to_json() for r in records]
    return {'frames': frames}


def get_frame(payload: dict):
    fid = payload.get('id')
    record = store.get_frame_by_id(fid)

    if not record:
        return {'error': 'not found'}

    frame = AppFrame.from_record(record)
    return {'frame': frame.to_json()}


def delete_frame(payload: dict):
    fid = payload.get('id')
    store.delete_frame(fid)
    send_telemetry("delete_frame", None)
    return {'ok': True}


def reorder_frames(payload: dict):
    order = payload.get('order', [])
    store.reorder_frames(order)
    send_telemetry("reorder_frames", None)
    return {'ok': True}


def transform_frame(payload: dict):
    op = payload.get('op')
    if not op:
        return {'error': 'op required'}

    rows = payload.get('rows')
    if rows is not None:
        frame = AppFrame.from_json({'rows': rows, 'brightness_levels': BRIGHTNESS_LEVELS})
    else:
        fid = payload.get('id')
        if fid is None:
            return {'error': 'id or rows required'}
        record = store.get_frame_by_id(fid)
        if not record:
            return {'error': 'frame not found'}
        frame = AppFrame.from_record(record)

    operations = {
        'invert': designer.invert,
        'invert_not_null': designer.invert_not_null,
        'rotate180': designer.rotate180,
        'flip_h': designer.flip_horizontally,
        'flip_v': designer.flip_vertically,
    }
    if op not in operations:
        return {'error': 'unsupported op'}

    operations[op](frame)
    send_telemetry("transform_frame", frame)
    return {'ok': True, 'frame': frame.to_json(), 'vector': frame.to_c_string()}


def export_frames(payload: dict = None):
    if payload and payload.get('frames'):
        frame_ids = [int(fid) for fid in payload['frames']]
        records = [store.get_frame_by_id(fid) for fid in frame_ids]
        records = [r for r in records if r is not None]
    else:
        records = store.list_frames(order_by='position ASC, id ASC')

    frames = [AppFrame.from_record(r) for r in records]

    animations = payload.get('animations') if payload else None

    if animations:
        header_parts = []
        for anim in animations:
            anim_name = anim.get('name', 'Animation')
            anim_frame_ids = anim.get('frames', [])
            anim_frames = [f for f in frames if f.id in anim_frame_ids]
            if not anim_frames:
                continue
            header_parts.append(f"// Animation: {anim_name}")
            header_parts.append(AppFrame.frames_to_c_animation_array(anim_frames, anim_name))
        header = "\n".join(header_parts).strip() + "\n"
        send_telemetry("export_frames", None)
        return {'header': header}
    else:
        header_parts = []
        for frame in frames:
            header_parts.append(f"// {frame.name} (id {frame.id})")
            header_parts.append(frame.to_c_string())
        header = "\n".join(header_parts).strip() + "\n"
        send_telemetry("export_frames", None)
        return {'header': header}


def play_animation_thread(animation_bytes):
    try:
        Bridge.call("play_animation", bytes(animation_bytes))
    except Exception:
        pass


def play_animation(payload: dict):
    frame_ids = payload.get('frames', [])
    loop = payload.get('loop', False)

    if not frame_ids:
        return {'error': 'no frames provided'}

    records = [store.get_frame_by_id(fid) for fid in frame_ids]
    records = [r for r in records if r is not None]

    if not records:
        return {'error': 'no valid frames found'}

    frames = [AppFrame.from_record(r) for r in records]

    animation_bytes = AppFrame.frames_to_animation_bytes(frames)

    thread = threading.Thread(target=play_animation_thread, args=(animation_bytes,))
    thread.start()

    send_telemetry("play_animation", None)
    return {'ok': True, 'frames_played': len(frames)}


def stop_animation(payload: dict = None):
    try:
        Bridge.call("stop_animation")
        send_telemetry("stop_animation", None)
        return {'ok': True}
    except Exception as e:
        return {'error': str(e)}


ui.expose_api('POST', '/update_board', update_board)
ui.expose_api('POST', '/persist_frame', persist_frame)
ui.expose_api('POST', '/load_frame', load_frame)
ui.expose_api('GET', '/list_frames', list_frames)
ui.expose_api('POST', '/get_frame', get_frame)
ui.expose_api('POST', '/delete_frame', delete_frame)
ui.expose_api('POST', '/transform_frame', transform_frame)
ui.expose_api('POST', '/export_frames', export_frames)
ui.expose_api('POST', '/reorder_frames', reorder_frames)
ui.expose_api('POST', '/play_animation', play_animation)
ui.expose_api('POST', '/stop_animation', stop_animation)
ui.expose_api('GET', '/config', get_config)

App.run()
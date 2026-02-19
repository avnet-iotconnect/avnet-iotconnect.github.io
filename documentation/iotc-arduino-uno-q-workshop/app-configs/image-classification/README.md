# /IOTCONNECT Version: image-classification

This is the /IOTCONNECT-enabled version of the Arduino example.

Original Arduino README:
- https://github.com/arduino/app-bricks-examples/blob/main/examples/image-classification/README.md

## Overview
This version adds an /IOTCONNECT relay client, a device template, and optional command handling so the app can publish telemetry and receive commands from /IOTCONNECT.

## What this adds
- /IOTCONNECT relay client wiring
- Device template for telemetry + commands
- Optional commands (if defined below)
- Optional debug logs for telemetry send

App Lab folder: `/home/arduino/ArduinoApps/classify-images`

## Files
- `python/main.py` (/IOTCONNECT-enabled app code)
- `config.json` (telemetry/command definitions)

## Device Template
This app uses the shared device template at `app-configs/arduino-app-lab-template.json`.
- Template code: `arduino`
- Template name: `arduino`

## Telemetry Fields
| Field | Type |
| --- | --- |
| `UnoQdemo` | `STRING` |
| `class_name` | `STRING` |
| `confidence` | `DECIMAL` |
| `processing_time_ms` | `INTEGER` |
| `input_type` | `STRING` |
| `image_type` | `STRING` |
| `results_json` | `STRING` |
| `status` | `STRING` |
| `top_class_name` | `STRING` |
| `top_confidence` | `DECIMAL` |

## Commands
| Command | Parameters |
| --- | --- |
| `set-confidence` | `confidence` |
| `classify-image` | `image_url`, `image`, `image_type`, `confidence` |

## Example /IOTCONNECT command payload
```json
{
  "image_url": "https://example.com/sample.jpg",
  "image_type": "jpeg",
  "confidence": 0.25
}
```

## How to use in App Lab
1) Copy the example into your App Lab workspace.
2) Copy the /IOTCONNECT-enabled python files into the app:
   ```bash
   cp /home/arduino/iotc-arduino-uno-q-workshop/app-configs/image-classification/python/* /home/arduino/ArduinoApps/classify-images/python/
   ```
3) Run the app and verify telemetry in /IOTCONNECT.

## Notes
- If the example sends telemetry only on user action, you will not see data until that action occurs.
- If you change the device template in /IOTCONNECT, re-create the device or update it to match these fields.

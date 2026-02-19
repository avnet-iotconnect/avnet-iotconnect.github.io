# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

import re
from arduino.app_bricks.cloud_llm import CloudLLM, CloudModel
from arduino.app_bricks.web_ui import WebUI
from arduino.app_utils import App

# ---- IOTCONNECT Relay ----
from iotc_relay_client import IoTConnectRelayClient

RELAY_ENDPOINT = "tcp://172.17.0.1:8899"
RELAY_CLIENT_ID = "bedtime_story_teller"
UNOQ_DEMO_NAME = "bedtime-story-teller"

relay = IoTConnectRelayClient(
    RELAY_ENDPOINT,
    client_id=RELAY_CLIENT_ID,
)
relay.start()


def send_telemetry(data, status="ok"):
    payload = {
        "UnoQdemo": UNOQ_DEMO_NAME,
        "age": str(data.get('age', 'any')),
        "theme": str(data.get('theme', 'any')),
        "tone": str(data.get('tone', 'any')),
        "ending_type": str(data.get('endingType', 'any')),
        "narrative_structure": str(data.get('narrativeStructure', 'any')),
        "duration": str(data.get('duration', 'any')),
        "character_count": int(len(data.get('characters', [])) if isinstance(data.get('characters', []), list) else 0),
        "status": status,
    }
    print("IOTCONNECT send:", payload)
    relay.send_telemetry(payload)


llm = CloudLLM(
    model=CloudModel.GOOGLE_GEMINI,
    system_prompt="You are a bedtime story teller. Your response must be the story itself, formatted directly in HTML. Do not wrap your response in markdown code blocks or any other formatting. Use heading tags like <h1>, <h2> for titles and subtitles. Use <strong> or <b> for bold text. Include relevant emojis. If the story is chapter-based, use heading tags for chapter titles.",
)
llm.with_memory()

ui = WebUI()


def generate_story(_, data):
    try:
        age = data.get('age', 'any')
        theme = data.get('theme', 'any')
        tone = data.get('tone', 'any')
        ending_type = data.get('endingType', 'any')
        narrative_structure = data.get('narrativeStructure', 'any')
        duration = data.get('duration', 'any')
        characters = data.get('characters', [])
        other = data.get('other', '')

        prompt_for_display = f"As a parent who loves to read bedtime stories to my <strong>{age}</strong> year old child, I need a delightful and age-appropriate story."

        if characters:
            prompt_for_display += " Characters of the story: "
            char_prompts = []
            for i, char in enumerate(characters):
                ch = f"Character {i+1} (<strong>{char.get('name')}</strong>, <strong>{char.get('role')}</strong>"
                ch += f", <strong>{char.get('description')}</strong>)" if char.get('description') else ")"
                char_prompts.append(ch)
            prompt_for_display += ", ".join(char_prompts)
            prompt_for_display += "."

        prompt_for_display += f" The story type is <strong>{theme}</strong>. The tone should be <strong>{tone}</strong>. The format should be a narrative-style story with a clear beginning, middle, and end, allowing for a smooth and engaging reading experience. The objective is to entertain and soothe the child before bedtime. Provide a brief introduction to set the scene and introduce the main character. The scope should revolve around the topic: managing emotions and conflicts. The length should be approximately <strong>{duration}</strong>. Please ensure the story has a <strong>{narrative_structure}</strong> narrative structure, leaving the child with a sense of <strong>{ending_type}</strong>. The language should be easy to understand and suitable for my child's age comprehension."
        if other:
            prompt_for_display += f"\n\nOther optional stuff for the story: <strong>{other}</strong>"

        prompt_for_llm = re.sub('<[^>]*>', '', prompt_for_display)

        ui.send_message("prompt", prompt_for_display)

        send_telemetry({
            'age': age,
            'theme': theme,
            'tone': tone,
            'endingType': ending_type,
            'narrativeStructure': narrative_structure,
            'duration': duration,
            'characters': characters,
        }, "requested")

        for resp in llm.chat_stream(prompt_for_llm):
            ui.send_message("response", resp)

        ui.send_message("stream_end", {})
        send_telemetry({
            'age': age,
            'theme': theme,
            'tone': tone,
            'endingType': ending_type,
            'narrativeStructure': narrative_structure,
            'duration': duration,
            'characters': characters,
        }, "complete")
    except Exception as e:
        ui.send_message("story_error", {"error": str(e)})
        send_telemetry(data or {}, f"error:{e}")

ui.on_message("generate_story", generate_story)

App.run()
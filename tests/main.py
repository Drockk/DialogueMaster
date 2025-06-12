import requests
import json
import psutil
import time
from utils import log_usage, save_chat_entry

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "dm"  # przykład modelu, może być inny

def send_notification(prompt, history=[], scenario_name="default"):
    return send_prompt(f"notification: {prompt}", history, scenario_name)

def send_dialog(dialog, history=[], scenario_name="default"):
    return send_prompt(dialog, history, scenario_name)

def send_prompt(prompt, history=[], scenario_name="default"):
    payload = {
        "model": MODEL,
        "messages": history + [{"role": "user", "content": prompt}],
        "stream": False
    }
    start_time = time.time()
    response = requests.post(OLLAMA_URL, json=payload)
    end_time = time.time()

    usage = log_usage(start_time, end_time)

    if response.ok:
        data = response.json()
        reply = data.get("message", {}).get("content", "")
        save_chat_entry(prompt, reply, usage, scenario_name)
        return reply
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

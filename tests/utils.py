import psutil
import json
import os
import time

HISTORY_FILE = "chat_history.json"

def log_usage(start_time, end_time):
    process = psutil.Process()
    cpu_percent = psutil.cpu_percent(interval=None)
    mem_info = process.memory_info()
    disk_usage = psutil.disk_usage('/')

    return {
        "duration_sec": end_time - start_time,
        "cpu_percent": cpu_percent,
        "rss_MB": mem_info.rss / (1024 * 1024),
        "disk_percent": disk_usage.percent
    }

def save_chat_entry(prompt, reply, usage, scenario_name):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt,
        "reply": reply,
        "usage": usage
    }

    filename = f"chat_history_{scenario_name}.json"

    if os.path.exists(filename):
        with open(filename, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2)


import json
import os
import uuid
import datetime

APPS_REGISTRY_FILE = "apps_registry.json"

def load_apps_registry():
    if os.path.exists(APPS_REGISTRY_FILE):
        try:
            with open(APPS_REGISTRY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_apps_registry(registry):
    with open(APPS_REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)

def add_app_to_registry(name, description, language, path, features=None, metadata=None):
    registry = load_apps_registry()
    app_entry = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "language": language,
        "path": os.path.abspath(path),
        "features": features or [],
        "metadata": metadata or {},
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    registry.append(app_entry)
    save_apps_registry(registry)

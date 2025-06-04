import json
import os
import re
from typing import Any
from pathlib import Path
from datetime import datetime

# Define export directory path
EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"

def safe_filename(name: str) -> str:
    """
    Sanitize the provided filename by replacing unsafe characters.
    """
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)

def export_to_json(data: Any, filename: str = None) -> None:
    """
    Export scan results to a JSON file.
    If no filename is provided, a timestamped one is generated automatically.
    """
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if filename:
        filename = safe_filename(filename)
        if not filename.endswith(".json"):
            filename += ".json"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scan_{timestamp}.json"

    full_path = EXPORT_DIR / filename

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"\nResults exported to: {full_path}")
    except Exception as e:
        print(f"Error while exporting to JSON: {e}")

def clean_exports() -> None:
    """
    Delete all JSON files inside the export directory.
    """
    if EXPORT_DIR.exists() and EXPORT_DIR.is_dir():
        deleted = 0
        for file in EXPORT_DIR.glob("**/*.json"):
            try:
                file.unlink()
                deleted += 1
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
        print(f"{deleted} JSON file(s) deleted.")
    else:
        print("No export directory found. Nothing to clean.")

def list_exports() -> None:
    """
    List all existing JSON export files in the export directory.
    Files are sorted by name in reverse order (newest first).
    """
    # Create the export directory if it doesn't exist
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    json_files = list(EXPORT_DIR.glob("*.json"))
    
    if not json_files:
        print("No JSON exports found.")
        return

    print("Existing exports:")
    for file in sorted(json_files, reverse=True):
        print(f"  - {file.name}")


import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# Define export directory path
EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"


def safe_filename(name: str) -> str:
    """
    Sanitize the provided filename by replacing unsafe characters.
    """
    return re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)


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
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\nResults exported to: {full_path}")
    except Exception as e:
        print(f"Error while exporting to JSON: {e}")


def export_to_csv(data: Any, host: str, filename: str = None) -> None:
    """
    Export scan results to a CSV file.
    If no filename is provided, a timestamped one is generated automatically.

    Args:
        data: The scan results dictionary.
        host: The target host.
        filename: The output filename.
    """
    import csv

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if filename:
        # Check if it's already a full path (e.g. from sanitize_export_path)
        path_obj = Path(filename)
        if path_obj.is_absolute():
            full_path = path_obj
        else:
            filename = safe_filename(filename)
            if not filename.endswith(".csv"):
                filename += ".csv"
            full_path = EXPORT_DIR / filename
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scan_{timestamp}.csv"
        full_path = EXPORT_DIR / filename

    try:
        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["host", "port", "status", "service", "banner"])

            # Flatten results
            for module_name, module_data in data.items():
                scan_results = module_data.get("scan_results", [])
                for entry in scan_results:
                    port = entry.get("port")
                    status = entry.get("status", "unknown")
                    service = entry.get("service", "N/A")
                    # Banner might not be present in all modules, but if it is, use it.
                    # For now, we'll leave it empty if not found, or try to extract from 'raw' if available?
                    # The user example showed 'banner', let's see if we have it.
                    # Looking at previous display logic, it doesn't explicitly show banner.
                    # But let's assume it might be in the entry or we leave it blank.
                    banner = entry.get("banner", "")
                    
                    writer.writerow([host, port, status, service, banner])

        print(f"\nResults exported to: {full_path}")
    except Exception as e:
        print(f"Error while exporting to CSV: {e}")


def load_json(filepath: str) -> Any:
    """
    Load data from a JSON file.

    Args:
        filepath: Path to the JSON file to load

    Returns:
        Loaded data from JSON file
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_exports() -> None:
    """
    Delete all JSON and CSV files inside the export directory.
    """
    if EXPORT_DIR.exists() and EXPORT_DIR.is_dir():
        deleted = 0
        for pattern in ["**/*.json", "**/*.csv"]:
            for file in EXPORT_DIR.glob(pattern):
                try:
                    file.unlink()
                    deleted += 1
                except Exception as e:
                    print(f"Failed to delete {file}: {e}")
        print(f"{deleted} file(s) deleted.")
    else:
        print("No export directory found. Nothing to clean.")


def list_exports() -> None:
    """
    List all existing JSON and CSV export files in the export directory.
    Files are sorted by name in reverse order (newest first).
    """
    # Create the export directory if it doesn't exist
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_files = list(EXPORT_DIR.glob("*.json"))
    csv_files = list(EXPORT_DIR.glob("*.csv"))
    all_files = json_files + csv_files

    if not all_files:
        print("No exports found.")
        return

    print("Existing exports:")
    for file in sorted(all_files, reverse=True):
        print(f"  - {file.name}")

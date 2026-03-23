import json
from datetime import datetime, timezone
from pathlib import Path


def fix_text(text):
    """Fix mojibake (Latin-1 misdecoded UTF-8)"""
    if not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text  # leave unchanged if it fails


def format_timestamp(ts_ms):
    """Convert milliseconds timestamp to readable format"""
    try:
        # Convert milliseconds to seconds and then format
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return ts_ms  # fallback if conversion fails


def process_messages(data):
    """Recursively fix all text fields in the JSON"""
    if isinstance(data, dict):
        # Remove unwanted fields
        data.pop("is_geoblocked_for_viewer", None)
        data.pop("is_unsent_image_by_messenger_kid_parent", None)

        if "timestamp_ms" in data and "content" not in data:
            return None

        # Remove message with "Liked a message"
        content = data.get("content")
        if content and (
            content == "Liked a message" or 
            "sent an attachment" in content or 
            "audio call" in content or 
            "Audio call" in content
        ):
            return None

        # Convert timestamp if present
        if "timestamp_ms" in data:
            data["timestamp_readable"] = format_timestamp(data["timestamp_ms"])

        # Recursively process the dictionary
        return {key: process_messages(value) for key, value in data.items()}
    elif isinstance(data, list):
        result = []
        for item in data:
            processed = process_messages(item)
            if processed is not None:
                result.append(processed)
        return result
    elif isinstance(data, str):
        return fix_text(data)
    else:
        return data


def main():
    INPUT_DIR = Path(
        "./data/zip/your_instagram_activity/messages/inbox/gina_828044388588461"
    )
    OUTPUT_DIR = Path("./data/decoded/gina/")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(1, 2):
        input_file = f"message_{i}.json"
        # Load JSON
        with open(INPUT_DIR / input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Fix encoding issues
        cleaned_data = process_messages(data)

        # Save cleaned JSON
        with open(OUTPUT_DIR / input_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        print(f"Cleaned file saved as: {OUTPUT_DIR / input_file}")

    INPUT_DIR = Path(
        "./data/zip/your_instagram_activity/messages/inbox/1_1259292115457383"
    )
    OUTPUT_DIR = Path("./data/decoded/1/")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(1, 19):
        input_file = f"message_{i}.json"
        # Load JSON
        with open(INPUT_DIR / input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Fix encoding issues
        cleaned_data = process_messages(data)

        # Save cleaned JSON
        with open(OUTPUT_DIR / input_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        print(f"Cleaned file saved as: {OUTPUT_DIR / input_file}")


if __name__ == "__main__":
    main()

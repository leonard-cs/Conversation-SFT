import json
from pathlib import Path


def load_messages(file_path):
    """Load messages from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("messages", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return []


def main():
    INPUT_FILE = Path("./data/decoded/") / "gina" / "message_1.json"
    OUTPUT_DIR = Path("./data/manual/")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE = OUTPUT_DIR / "gina_manual.jsonl"

    messages = load_messages(INPUT_FILE)
    messages = list(reversed(messages))

    # Keep only desired fields
    filtered = [
        {"sender": m.get("sender_name"), "content": m.get("content")}
        for m in messages
        if m.get("content")  # optional: skip empty messages
    ]

    # Write JSONL (one JSON object per line)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for msg in filtered:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    print(f"Generated {len(filtered)} messages in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

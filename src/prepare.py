import json
from pathlib import Path

import icecream

# Parameters
MY_NAME = "Leonard Chi"
K_CONTEXT = 10  # number of previous messages to use as context


def load_messages(file_path):
    """Load messages from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("messages", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file {file_path}: {e}")
        return []


def merge_consecutive_messages(messages, senders_to_merge):
    """Merge consecutive messages from specified senders into one message, separated by newlines."""
    merged_messages = []
    previous_message = None

    for msg in messages:
        if "content" not in msg:
            icecream.ic(msg)
        # Check if the sender is in the list of senders to merge
        if (
            previous_message
            and msg["sender_name"] == previous_message["sender_name"]
            and msg["sender_name"] in senders_to_merge
        ):
            # Append the content of the current message to the previous one
            previous_message["content"] += "\n" + msg["content"]
        else:
            # If not the same sender, push the previous message to the list and reset
            if previous_message:
                merged_messages.append(previous_message)
            previous_message = msg.copy()

    # Append the last message if any
    if previous_message:
        merged_messages.append(previous_message)

    return merged_messages


def build_examples(messages, my_name, k):
    """Build fine-tuning examples from messages."""
    examples = []
    messages = merge_consecutive_messages(messages, [my_name])

    for i, msg in enumerate(messages):
        if msg.get("sender_name") == my_name and "content" in msg:
            # Collect k previous messages as context
            start_idx = max(0, i - k)
            conversations = messages[start_idx : i + 1]

            # Skip assistant messages at the beginning of the conversation
            for j, m in enumerate(conversations):
                if m.get("sender_name") != my_name:
                    conversations = conversations[
                        j:
                    ]  # Start from the first user message
                    break
            else:
                # No user message found, skip this example
                continue

            # Build conversation data
            data = []
            for m in conversations:
                if "content" in m:
                    role = "user" if m["sender_name"] != my_name else "assistant"
                    data.append({"role": role, "content": m["content"]})

            examples.append({"messages": data})

    return examples


def main():
    INPUT_DIR = Path("./data/decoded/")
    OUTPUT_DIR = Path("./data/auto-data/")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE = OUTPUT_DIR / "fine_tune_examples.jsonl"

    all_examples = []

    file_path = INPUT_DIR / "gina" / "message_1.json"

    messages = load_messages(file_path)
    messages = list(reversed(messages))
    examples = build_examples(messages, MY_NAME, K_CONTEXT)
    all_examples.extend(examples)

    INPUT_FILES = []
    for i in range(1, 19):
        INPUT_FILES.append(INPUT_DIR / "1" / f"message_{i}.json")
    # Load and process each JSON file
    all_messages = []
    for file_path in INPUT_FILES:
        messages = load_messages(file_path)
        messages = list(reversed(messages))
        all_messages.extend(messages)
    examples = build_examples(all_messages, MY_NAME, K_CONTEXT)
    all_examples.extend(examples)

    # Save examples to JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ex in all_examples:
            json.dump(ex, f, ensure_ascii=False)
            f.write("\n")

    print(f"Generated {len(all_examples)} training examples in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

from src.prepare import merge_consecutive_messages
# def merge_consecutive_messages(messages, senders_to_merge):
#     """Merge consecutive messages from specified senders into one message, separated by newlines."""
#     merged_messages = []
#     previous_message = None
    
#     for msg in messages:
#         # Check if the sender is in the list of senders to merge
#         if previous_message and msg["sender_name"] == previous_message["sender_name"] and msg["sender_name"] in senders_to_merge:
#             # Append the content of the current message to the previous one
#             previous_message["content"] += "\n" + msg["content"]
#         else:
#             # If not the same sender, push the previous message to the list and reset
#             if previous_message:
#                 merged_messages.append(previous_message)
#             previous_message = msg

#     # Append the last message if any
#     if previous_message:
#         merged_messages.append(previous_message)

#     return merged_messages

merge_sample_messages = [
    {
        "sender_name": "Joe",
        "timestamp_ms": 1760476016075,
        "content": "Joe message1",
        "call_duration": 3479,
        "timestamp_readable": "2025-10-14 21:06:56 UTC",
    },
    {
        "sender_name": "Joe",
        "timestamp_ms": 1760475588557,
        "content": "Joe message2",
        "timestamp_readable": "2025-10-14 20:59:48 UTC",
    },
    {
        "sender_name": "Tom",
        "timestamp_ms": 1760473967745,
        "content": "Tom message1",
        "timestamp_readable": "2025-10-14 20:32:47 UTC",
    },
    {
        "sender_name": "Tom",
        "timestamp_ms": 1760473430627,
        "content": "Tom message2",
        "timestamp_readable": "2025-10-14 20:23:50 UTC",
    },
]


def test_merge_consecutive_messages_joe_only():
    merged = merge_consecutive_messages(merge_sample_messages, ["Joe"])

    assert len(merged) == 3
    assert merged[0]["sender_name"] == "Joe"
    assert merged[0]["content"] == "Joe message1\nJoe message2"
    assert merged[1]["sender_name"] == "Tom"
    assert merged[1]["content"] == "Tom message1"
    assert merged[2]["sender_name"] == "Tom"
    assert merged[2]["content"] == "Tom message2"


def test_merge_consecutive_messages_joe_and_tom():
    merged = merge_consecutive_messages(merge_sample_messages, ["Joe", "Tom"])
    
    assert len(merged) == 2
    assert merged[0]["sender_name"] == "Joe"
    assert merged[0]["content"] == "Joe message1\nJoe message2"
    assert merged[1]["sender_name"] == "Tom"
    assert merged[1]["content"] == "Tom message1\nTom message2"


def test_merge_consecutive_messages_joe_tom_and_leo():
    merged = merge_consecutive_messages(merge_sample_messages, ["Joe", "Tom", "Leo"])
    print(merged)
    
    assert len(merged) == 2
    assert merged[0]["sender_name"] == "Joe"
    assert merged[0]["content"] == "Joe message1\nJoe message2"
    assert merged[1]["sender_name"] == "Tom"
    assert merged[1]["content"] == "Tom message1\nTom message2"

test_merge_consecutive_messages_joe_and_tom()
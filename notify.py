#!/usr/bin/env python3
"""Play a random Warcraft 3 quote."""

import json
import random
import subprocess
import sys
from pathlib import Path

ENABLE_JSON_ARG_FILES = True
SKIP_INTERNAL_TITLE_EVENTS = True
INTERNAL_TITLE_PROMPT_PREFIX = "You are a helpful assistant."
INTERNAL_TITLE_PROMPT_MARKER = "your job is to provide a short title for a task"


def write_json_arg_file(root_dir, notification_arg):
    existing_indexes = [
        int(path.stem.removeprefix("json-arg")) for path in root_dir.glob("json-arg*.json")
    ]
    index = max(existing_indexes) + 1 if existing_indexes else 0
    (root_dir / f"json-arg{index}.json").write_text(notification_arg)


def is_internal_title_event(notification):
    input_messages = notification["input-messages"]
    if len(input_messages) != 1:
        return False
    prompt = input_messages[0]
    if not prompt.startswith(INTERNAL_TITLE_PROMPT_PREFIX):
        return False
    if INTERNAL_TITLE_PROMPT_MARKER not in prompt:
        return False
    title_response = json.loads(notification["last-assistant-message"])
    return isinstance(title_response, dict) and set(title_response) == {"title"}


def main():
    root_dir = Path(__file__).resolve().parent
    notification_arg = sys.argv[1]
    if ENABLE_JSON_ARG_FILES:
        write_json_arg_file(root_dir, notification_arg)

    notification = json.loads(notification_arg)
    if SKIP_INTERNAL_TITLE_EVENTS and is_internal_title_event(notification):
        return

    quotes_dir = root_dir / "quotes"
    quote_path = random.choice(list(quotes_dir.glob("*.qta")))
    subprocess.run(["afplay", str(quote_path)], check=True)


if __name__ == "__main__":
    main()

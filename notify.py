#!/usr/bin/env python3
"""Play a random Warcraft 3 quote."""

import fcntl
import json
import random
import subprocess
import sys
from pathlib import Path

ENABLE_JSON_ARG_FILES = False


def write_json_arg_file(root_dir, hook_input):
    existing_indexes = [
        int(path.stem.removeprefix("json-arg")) for path in root_dir.glob("json-arg*.json")
    ]
    index = max(existing_indexes) + 1 if existing_indexes else 0
    formatted_hook_input = json.dumps(hook_input, indent=2)
    (root_dir / f"json-arg{index}.json").write_text(f"{formatted_hook_input}\n")


def read_hook_input():
    return json.loads(sys.stdin.read())


def is_title_generation_stop(hook_input):
    if hook_input["hook_event_name"] != "Stop":
        return False
    if hook_input["transcript_path"] is not None:
        return False

    message = json.loads(hook_input["last_assistant_message"])
    return set(message) == {"title"}


def play_quote(root_dir):
    quotes_dir = root_dir / "quotes"
    quote_path = random.choice(list(quotes_dir.glob("*.qta")))
    lock_path = root_dir / ".audio-queue.lock"
    with lock_path.open("w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        subprocess.run(["afplay", str(quote_path)], check=True)


def main():
    root_dir = Path(__file__).resolve().parent
    hook_input = read_hook_input()
    if ENABLE_JSON_ARG_FILES:
        write_json_arg_file(root_dir, hook_input)

    if is_title_generation_stop(hook_input):
        return

    play_quote(root_dir)


if __name__ == "__main__":
    main()

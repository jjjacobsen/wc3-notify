#!/usr/bin/env python3
"""Play a random Warcraft 3 quote."""

import random
import subprocess
from pathlib import Path


def main():
    quotes_dir = Path(__file__).resolve().parent / "quotes"
    quote_path = random.choice(list(quotes_dir.glob("*.qta")))
    subprocess.run(["afplay", str(quote_path)], check=True)


if __name__ == "__main__":
    main()

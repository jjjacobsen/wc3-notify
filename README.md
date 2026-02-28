# wc3_notify

Play a Warcraft 3 quote when `notify.py` runs.

## Files

- `notify.py`: Script entry point (run on Codex turn completion).
- `quotes/`: Directory of audio quote files that are played by the script.

## Setup

Place your legally obtained Warcraft III sound files in `quotes/`.

Put this at the top of `~/.codex/config.toml`:

```toml
# 🔔 Play sound when agent turn completes
notify = ["python3", "/full/path/to/notify.py"]
```

## Notes

This works for both the Codex App and Codex CLI

For now (it will probably get fixed) there is a notification that gets emitted by the app for setting the title of the thread. `notify.py` will attempt to detect this fake notification and skip it

The [Codex notification documentation](https://developers.openai.com/codex/config-advanced/#notifications) explains the JSON argument provided to notify and what is contained in the JSON

## Increase Volume For All Quotes

Use this to apply a `+12dB` gain to every `.qta` file in `quotes/`, replacing each file in place:

```bash
for f in quotes/*.qta; do tmp="$(mktemp "${f%.qta}.tmp.XXXXXX.qta")"; ffmpeg -hide_banner -y -i "$f" -map 0:a:0 -af "volume=12dB" -c:a aac -b:a 192k -f ipod "$tmp" && mv "$tmp" "$f" || exit 1; done
```

What it does:

- Processes each quote one-by-one with `ffmpeg`.
- Uses only `volume=12dB` (no denoise/compression/normalization).
- Writes to a temp file first, then moves it over the original file.
- Stops immediately if any file fails.

When to use it:

- Your quotes are consistently too quiet.
- You want a simple loudness boost without changing tone/character.

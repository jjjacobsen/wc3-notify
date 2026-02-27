# wc3_notify

Play a Warcraft 3 quote when `notify.py` runs.

## Files

- `notify.py`: Script entry point (run on Codex turn completion).
- `quotes/`: Directory of audio quote files that are played by the script.

## Setup

### Notes

Place your legally obtained Warcraft III sound files in `quotes/`.

Put this at the top of `~/.codex/config.toml`:

```toml
# 🔔 Play sound when agent turn completes
notify = ["python3", "/full/path/to/notify.py"]
```

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

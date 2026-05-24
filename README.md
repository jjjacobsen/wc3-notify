# wc3_notify

Play a Warcraft 3 quote from Codex hooks.

## Files

- `notify.py`: Script entry point for Codex hooks.
- `quotes/`: Directory of audio quote files that are played by the script.

## Setup

Place your legally obtained Warcraft III sound files in `quotes/`.

For custom clips, use `yt-dlp` to get source audio and `ffmpeg` to trim or convert it into whatever audio file you would like in `quotes/`.

Enable hooks and add this to `~/.codex/config.toml`:

```toml
[features]
hooks = true

[[hooks.PermissionRequest]]
[[hooks.PermissionRequest.hooks]]
type = "command"
command = 'python3 "/full/path/to/notify.py"'
timeout = 30
statusMessage = "Playing approval sound"

[[hooks.Stop]]
[[hooks.Stop.hooks]]
type = "command"
command = 'python3 "/full/path/to/notify.py"'
timeout = 30
statusMessage = "Playing finished sound"
```

## Notes

Codex may ask you to review and trust the hook definition before it runs. Use the Hooks settings or `/hooks` in the CLI if it is marked untrusted

The [Codex hook documentation](https://developers.openai.com/codex/hooks) explains the hook input provided on stdin

Codex can run a background title-generation turn for a new chat. That turn can trigger a `Stop` hook with no transcript path and a JSON assistant message like `{"title":"First chat prompt"}`. `notify.py` skips that title-generation `Stop` hook so the first real assistant response still plays a completion quote

Set `ENABLE_JSON_ARG_FILES = True` in `notify.py` to capture hook input as `json-arg*.json` files when debugging hook behavior. Turn it back off after capturing the payloads

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

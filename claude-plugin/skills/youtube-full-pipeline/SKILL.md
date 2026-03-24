# YouTube Full Pipeline

End-to-end automation: generate a YouTube Short video AND upload it to YouTube.

## What This Does

Combines the `youtube-generate` and `youtube-upload` skills into a single operation:

1. Generate topic → script → metadata → image prompts → images → TTS → subtitles → video
2. Upload the generated video to YouTube via Selenium
3. Cache the uploaded video metadata

## How to Run

```bash
cd /home/user/MoneyPrinterV2
python src/cron.py youtube <account_uuid> <ollama_model>
```

This is the simplest way to run the full pipeline. It:
- Looks up the account from `.mp/youtube.json`
- Sets the Ollama model
- Calls `YouTube.generate_video()` then `YouTube.upload_video()`

### Finding Account UUID and Model

```bash
# List YouTube accounts
python claude-plugin/scripts/list-accounts.py --provider youtube

# List available Ollama models
python claude-plugin/scripts/list-models.py
```

## Prerequisites

All prerequisites from both `youtube-generate` and `youtube-upload` apply:
- Ollama running with model pulled
- Gemini API key configured
- ImageMagick installed
- Firefox profile pre-authenticated to YouTube
- Background music in `Songs/`

Run preflight: `python scripts/preflight_local.py`

## Example Workflow

```
User: "Make a cooking video and upload it"

1. Check if account exists → list-accounts.py
2. Check if setup is ready → preflight_local.py
3. Run full pipeline → python src/cron.py youtube <uuid> <model>
4. Report the uploaded video URL
```

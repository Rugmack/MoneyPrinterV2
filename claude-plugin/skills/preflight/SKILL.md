# Preflight Check

Validate that the MoneyPrinterV2 setup is ready to run.

## How to Run

```bash
cd /home/user/MoneyPrinterV2
python scripts/preflight_local.py
```

## What It Checks

| Check | Required For |
|-------|-------------|
| `config.json` exists | Everything |
| `imagemagick_path` valid | Video subtitle rendering |
| `firefox_profile` exists | YouTube upload, Twitter |
| Ollama server reachable | LLM text generation |
| Ollama has models | LLM text generation |
| `nanobanana2_api_key` set | Image generation |
| Nano Banana 2 API reachable | Image generation |
| `faster-whisper` installed | Local STT (if stt_provider=local_whisper) |

## Interpreting Results

- `[OK]` — Check passed
- `[WARN]` — Non-blocking issue (feature may not work)
- `[FAIL]` — Blocking issue (must fix before running)

## Quick Fixes

### Missing config.json
```bash
cp config.example.json config.json
# Then edit config.json with your values
```

### Ollama not running
```bash
ollama serve &
ollama pull llama3.2:3b  # or your preferred model
```

### Missing Gemini API key
Set in config.json as `nanobanana2_api_key` or export `GEMINI_API_KEY` environment variable.

### macOS Quick Setup
```bash
bash scripts/setup_local.sh
```
This auto-configures Ollama, ImageMagick, and Firefox profile on macOS.

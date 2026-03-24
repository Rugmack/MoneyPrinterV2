# YouTube Shorts Generator

Generate a YouTube Short video using MoneyPrinterV2's pipeline.

## Pipeline Overview

The video generation pipeline runs these steps in order:
1. **Generate Topic** — LLM creates a one-sentence video idea based on the channel's niche
2. **Generate Script** — LLM writes a short script (configurable sentence count)
3. **Generate Metadata** — LLM produces title (< 100 chars with hashtags) + description
4. **Generate Image Prompts** — LLM creates JSON array of image generation prompts
5. **Generate Images** — Nano Banana 2 (Gemini API) creates images from prompts
6. **Text-to-Speech** — KittenTTS synthesizes the script to WAV audio
7. **Generate Subtitles** — Whisper (local) or AssemblyAI transcribes audio to SRT
8. **Combine** — MoviePy composites images + audio + subtitles + background music into MP4

## How to Run

### Option A: Non-interactive helper script (Recommended)

```bash
cd /home/user/MoneyPrinterV2
python claude-plugin/scripts/generate-video.py --account-id <UUID> --model <ollama_model>
```

The script will:
- Look up the account from `.mp/youtube.json`
- Run the full generation pipeline
- Output the path to the generated MP4

### Option B: Headless via cron.py (generates AND uploads)

```bash
cd /home/user/MoneyPrinterV2
python src/cron.py youtube <account_uuid> <ollama_model>
```

**Note:** cron.py always uploads after generating. Use the helper script if you only want generation.

## Prerequisites

Before running, verify:
1. `config.json` exists with valid settings
2. Ollama is running and the model is pulled
3. `nanobanana2_api_key` is set (or `GEMINI_API_KEY` env var)
4. `imagemagick_path` points to a valid ImageMagick binary
5. At least one YouTube account is registered in `.mp/youtube.json`
6. Background music exists in `Songs/` directory

Run the preflight check: `python scripts/preflight_local.py`

## Key Config Options

| Key | Purpose | Default |
|-----|---------|---------|
| `ollama_model` | LLM model name | (must be set) |
| `nanobanana2_api_key` | Gemini image API key | (must be set) |
| `nanobanana2_model` | Image model | `gemini-3.1-flash-image-preview` |
| `nanobanana2_aspect_ratio` | Image aspect ratio | `9:16` |
| `tts_voice` | TTS voice name | `Jasper` |
| `stt_provider` | STT backend | `local_whisper` |
| `script_sentence_length` | Script sentences | `4` |
| `font` | Subtitle font | (from config) |
| `threads` | MoviePy render threads | (from config) |

## Output

- Generated MP4: `.mp/<uuid>.mp4`
- Temporary files (images, audio, subtitles) are in `.mp/` and cleaned on next run

## Troubleshooting

- **"No models found on Ollama"** → Run `ollama pull <model-name>` first
- **Image generation fails** → Check `nanobanana2_api_key` in config.json
- **Subtitle generation fails** → Video still generates, just without subtitles
- **"Firefox profile path does not exist"** → Update the account's `firefox_profile` path

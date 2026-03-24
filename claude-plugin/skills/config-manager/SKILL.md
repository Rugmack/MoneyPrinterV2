# Config Manager

View and edit MoneyPrinterV2's `config.json` settings.

## Config File Location

```
/home/user/MoneyPrinterV2/config.json
```

Template: `config.example.json`

## Reading Config

To view the current configuration:
```bash
cat /home/user/MoneyPrinterV2/config.json | python -m json.tool
```

Or use the Read tool to read `config.json` directly.

## Editing Config

Use the Edit tool to modify specific values in `config.json`. The file is standard JSON.

**NEVER overwrite the entire file** — always use targeted edits to change specific keys.

## Key Configuration Groups

### LLM (Ollama)
| Key | Type | Description |
|-----|------|-------------|
| `ollama_base_url` | string | Ollama server URL (default: `http://127.0.0.1:11434`) |
| `ollama_model` | string | Model name (e.g., `llama3.2:3b`). If empty, user picks at startup. |

### Image Generation (Nano Banana 2 / Gemini)
| Key | Type | Description |
|-----|------|-------------|
| `nanobanana2_api_key` | string | Gemini API key (or use `GEMINI_API_KEY` env var) |
| `nanobanana2_model` | string | Model (default: `gemini-3.1-flash-image-preview`) |
| `nanobanana2_aspect_ratio` | string | Aspect ratio (default: `9:16`) |
| `nanobanana2_api_base_url` | string | API base URL |

### Browser Automation
| Key | Type | Description |
|-----|------|-------------|
| `firefox_profile` | string | Default Firefox profile path |
| `headless` | boolean | Run browser in headless mode |

### TTS & STT
| Key | Type | Description |
|-----|------|-------------|
| `tts_voice` | string | Voice name (default: `Jasper`) |
| `stt_provider` | string | `local_whisper` or `third_party_assemblyai` |
| `whisper_model` | string | Whisper model (default: `base`) |
| `whisper_device` | string | Device (default: `auto`) |
| `whisper_compute_type` | string | Compute type (default: `int8`) |
| `assembly_ai_api_key` | string | AssemblyAI API key |

### Video Rendering
| Key | Type | Description |
|-----|------|-------------|
| `imagemagick_path` | string | Path to ImageMagick binary |
| `threads` | integer | MoviePy render threads |
| `font` | string | Subtitle font filename |
| `script_sentence_length` | integer | Number of sentences in generated scripts (default: 4) |

### YouTube
| Key | Type | Description |
|-----|------|-------------|
| `is_for_kids` | boolean | YouTube "made for kids" flag |
| `zip_url` | string | Background music archive URL |

### Other
| Key | Type | Description |
|-----|------|-------------|
| `verbose` | boolean | Enable verbose logging |
| `twitter_language` | string | Language for Twitter posts |

## Safety Rules

- **NEVER** commit `config.json` to git (it contains API keys)
- **NEVER** log or display API keys in output
- Always validate JSON syntax after edits

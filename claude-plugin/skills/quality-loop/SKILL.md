# Video Quality Improvement Loop

Iteratively generate, review, and improve YouTube Shorts by using Gemini as a video quality reviewer. The loop focuses on **visual realism** and **viewer immersion**.

## Flow

```
Generate → Upload (public) → Get URL
  → Send URL to Gemini → Get JSON feedback
  → Set video to unlisted
  → If "approve": done (ask user to re-publish)
  → If "revise": apply fixes → loop back (max 3 iterations)
```

## Step-by-Step

### Step 1: Generate Video

```bash
cd /home/user/MoneyPrinterV2
python claude-plugin/scripts/generate-video.py --account-id <UUID> --model <model>
```

Capture `OUTPUT_VIDEO_PATH=<path>` from stdout. Also note the generated script text and niche from the account for later use.

### Step 2: Upload as Public

```bash
python claude-plugin/scripts/upload-video.py \
  --account-id <UUID> \
  --video-path <path from step 1> \
  --title "<title>" \
  --description "<description>" \
  --visibility public
```

Capture `OUTPUT_VIDEO_URL=<url>` from stdout.

### Step 3: Review via Gemini

```bash
python claude-plugin/scripts/review-video.py \
  --video-url "<url from step 2>" \
  --niche "<channel niche>" \
  --script "<the generated script>"
```

Capture `REVIEW_JSON=<json>` from stdout. Parse it.

### Step 4: Set Video to Unlisted

Immediately after receiving the review, hide the video:

```bash
python claude-plugin/scripts/set-video-visibility.py \
  --account-id <UUID> \
  --video-url "<url>" \
  --visibility unlisted
```

### Step 5: Evaluate

Parse the review JSON:
- `overall_score >= 7` AND `verdict == "approve"` → **Done.** Ask the user if they want to re-publish the video as public.
- `verdict == "revise"` → Continue to Step 6.
- **Max 3 iterations.** If reached, present the best-scoring video to the user.

### Step 6: Apply Improvements

Use the `parameter_adjustments` array from the review JSON to make targeted changes. Always show the user what you plan to change before applying.

#### Feedback → Code Change Mapping

Search for the pattern (not just line number) since lines may shift:

| Feedback area | What to search | File |
|---|---|---|
| Images look AI-generated | `"Please generate"` prompt for image descriptions | `src/classes/YouTube.py` (search `n_prompts`) |
| Subtitles hard to read | `fontsize=`, `color=`, `stroke_width=` | `src/classes/YouTube.py` (search `fontsize`) |
| BGM too loud | `volumex` | `src/classes/YouTube.py` (search `volumex`) |
| Pacing too fast/slow | `n_prompts = len` (controls image count) | `src/classes/YouTube.py` (search `n_prompts`) |
| Script not engaging | Script generation prompt with `sentence` | `src/classes/YouTube.py` (search `generate_script`) |
| No transitions/abrupt cuts | `fadein` (commented out) | `src/classes/YouTube.py` (search `fadein`) |
| Script too short/long | `script_sentence_length` | `config.json` |
| TTS voice doesn't fit | `tts_voice` | `config.json` |

#### Rules for applying changes:
1. **Track originals**: Before editing any file, note the original value so it can be reverted.
2. **Small steps**: Change one or two parameters at a time, not everything at once.
3. **Conservative**: Adjust by small increments (e.g., font size 100 → 90, not 100 → 40).

### Step 7: Regenerate

Go back to Step 1. The temp files are cleaned automatically by `rem_temp_files()`.

## After the Loop

- If the final video is approved, ask the user whether to:
  - Re-publish it as public
  - Keep it unlisted
- Ask the user whether to **keep** or **revert** the code/config changes made during the loop.
- Report the score trajectory across iterations (e.g., "5 → 6 → 8").

## Example Session

```
User: "Generate a cooking video and optimize it for realism"

Iteration 1:
  Generate → Upload (public) → URL: https://youtube.com/shorts/abc123
  Review → Score 5/10, verdict "revise"
    realism: 4/10 — "images have visible AI artifacts, text in images is garbled"
    immersion: 6/10 — "BGM overpowers narration"
  Set to unlisted
  Apply: Enhance image prompt to add "photorealistic, no text overlays"
         BGM volume 0.1 → 0.05

Iteration 2:
  Generate → Upload (public) → URL: https://youtube.com/shorts/def456
  Review → Score 7/10, verdict "approve"
    realism: 7/10, immersion: 7/10
  Set to unlisted
  Done. Ask user to re-publish.

Score trajectory: 5 → 7
```

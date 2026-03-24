# YouTube Upload

Upload a previously generated video to YouTube using Selenium browser automation.

## How It Works

The upload process uses a pre-authenticated Firefox profile to:
1. Navigate to YouTube Studio and extract the channel ID
2. Go to youtube.com/upload
3. Select the video file via the file picker
4. Fill in title and description from generated metadata
5. Set "made for kids" option
6. Click through the upload wizard (3 "next" buttons)
7. Set visibility to "unlisted"
8. Click "done"
9. Retrieve the uploaded video URL from YouTube Studio
10. Cache the video metadata in `.mp/youtube.json`

## How to Run

### Option A: Helper script (upload only)

```bash
cd /home/user/MoneyPrinterV2
python claude-plugin/scripts/upload-video.py --account-id <UUID> --video-path <path-to-mp4> --title "Video Title" --description "Video description"
```

### Option B: Full pipeline via cron.py (generate + upload)

```bash
cd /home/user/MoneyPrinterV2
python src/cron.py youtube <account_uuid> <ollama_model>
```

## Prerequisites

1. A YouTube account registered in `.mp/youtube.json` with a valid `firefox_profile` path
2. The Firefox profile must be **pre-logged-in** to YouTube (the plugin never handles login)
3. `headless` in config.json controls whether the browser runs visibly or headless
4. A generated video MP4 file

## Important Notes

- The browser must NOT be running with the same Firefox profile simultaneously
- Upload takes ~30-60 seconds depending on video size and network
- Videos are uploaded as **unlisted** by default
- The `is_for_kids` config flag controls YouTube's "made for kids" setting
- After upload, the video URL is cached in the account's `videos` array

## Troubleshooting

- **Browser crashes** → Close any running Firefox instances first
- **Login required** → Re-authenticate the Firefox profile manually, then retry
- **Element not found** → YouTube UI may have changed; selectors in `src/constants.py` may need updating

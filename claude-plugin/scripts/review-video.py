#!/usr/bin/env python3
"""Send a YouTube video URL to Gemini for quality review.

Usage:
    python claude-plugin/scripts/review-video.py --video-url <url> [--model gemini-2.5-flash] [--niche <niche>] [--script <script>]

Must be run from the MoneyPrinterV2 project root.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from config import get_nanobanana2_api_key, get_nanobanana2_api_base_url, get_gemini_review_model
from status import error, info

try:
    import requests
except ImportError:
    print("requests library required", file=sys.stderr)
    sys.exit(1)

REVIEW_PROMPT = """You are a YouTube Shorts quality reviewer specializing in visual realism and viewer immersion.

Watch this video and evaluate it:
Video URL: {video_url}
Channel niche: {niche}
Original script: {script}

Focus on these two core criteria:
1. REALISM — Do the images and video look realistic and natural? Are there AI artifacts, uncanny elements, or visual inconsistencies?
2. IMMERSION — Would a human viewer be drawn in and stay engaged? Does the pacing, audio, and visual flow create a compelling experience?

Return ONLY a JSON object with this exact structure:
{{
  "overall_score": <1-10>,
  "verdict": "approve" or "revise",
  "realism": {{
    "score": <1-10>,
    "issues": ["specific problems with realism"],
    "suggestions": ["specific improvements"]
  }},
  "immersion": {{
    "score": <1-10>,
    "issues": ["what breaks immersion"],
    "suggestions": ["how to improve engagement"]
  }},
  "parameter_adjustments": [
    {{
      "parameter": "<name>",
      "current_behavior": "<what it does now>",
      "recommended_value": "<new value>",
      "rationale": "<why>"
    }}
  ]
}}"""


def main():
    parser = argparse.ArgumentParser(description="Review a YouTube video via Gemini")
    parser.add_argument("--video-url", required=True, help="YouTube video URL")
    parser.add_argument("--model", default=None, help="Gemini model (default: from config)")
    parser.add_argument("--niche", default="general", help="Channel niche for context")
    parser.add_argument("--script", default="(not provided)", help="Original script text")
    args = parser.parse_args()

    api_key = get_nanobanana2_api_key()
    if not api_key:
        error("Gemini API key not configured. Set nanobanana2_api_key in config.json or GEMINI_API_KEY env var.")
        sys.exit(1)

    base_url = get_nanobanana2_api_base_url()
    model = args.model or get_gemini_review_model()

    prompt = REVIEW_PROMPT.format(
        video_url=args.video_url,
        niche=args.niche,
        script=args.script,
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
        },
    }

    url = f"{base_url}/models/{model}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }

    info(f"Sending video to {model} for review...")

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.RequestException as e:
        error(f"Gemini API request failed: {e}")
        sys.exit(1)

    data = resp.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        review = json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        error(f"Failed to parse Gemini response: {e}")
        print(json.dumps(data, indent=2), file=sys.stderr)
        sys.exit(1)

    info(f"Review complete. Score: {review.get('overall_score', '?')}/10, Verdict: {review.get('verdict', '?')}")
    print(f"REVIEW_JSON={json.dumps(review)}")


if __name__ == "__main__":
    main()

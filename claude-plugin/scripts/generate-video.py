#!/usr/bin/env python3
"""Non-interactive YouTube Short video generator for Claude Code plugin.

Usage:
    python claude-plugin/scripts/generate-video.py --account-id <UUID> --model <ollama_model>

Must be run from the MoneyPrinterV2 project root.
"""
import argparse
import os
import sys

# Add src/ to path (same as src/main.py does)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from cache import get_accounts
from config import assert_folder_structure
from utils import rem_temp_files, fetch_songs
from classes.Tts import TTS
from classes.YouTube import YouTube
from llm_provider import select_model
from status import success, error, info


def main():
    parser = argparse.ArgumentParser(description="Generate a YouTube Short video")
    parser.add_argument("--account-id", required=True, help="YouTube account UUID")
    parser.add_argument("--model", required=True, help="Ollama model name")
    args = parser.parse_args()

    # Setup
    assert_folder_structure()
    rem_temp_files()
    fetch_songs()
    select_model(args.model)

    # Find account
    accounts = get_accounts("youtube")
    account = None
    for acc in accounts:
        if acc["id"] == args.account_id:
            account = acc
            break

    if account is None:
        error(f"Account not found: {args.account_id}")
        print("Available accounts:")
        for acc in accounts:
            print(f"  {acc['id']}  {acc['nickname']}  ({acc['niche']})")
        sys.exit(1)

    info(f"Generating video for account: {account['nickname']} (niche: {account['niche']})")

    youtube = YouTube(
        account["id"],
        account["nickname"],
        account["firefox_profile"],
        account["niche"],
        account["language"],
    )

    tts = TTS()
    video_path = youtube.generate_video(tts)

    success(f"Video generated: {video_path}")
    # Print path to stdout for programmatic use
    print(f"OUTPUT_VIDEO_PATH={video_path}")


if __name__ == "__main__":
    main()

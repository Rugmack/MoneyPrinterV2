#!/usr/bin/env python3
"""Non-interactive YouTube video uploader for Claude Code plugin.

Usage:
    python claude-plugin/scripts/upload-video.py --account-id <UUID> --video-path <path> --title "Title" --description "Desc"

Must be run from the MoneyPrinterV2 project root.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from cache import get_accounts
from classes.YouTube import YouTube
from status import success, error, info


def main():
    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument("--account-id", required=True, help="YouTube account UUID")
    parser.add_argument("--video-path", required=True, help="Path to MP4 file")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", required=True, help="Video description")
    args = parser.parse_args()

    if not os.path.isfile(args.video_path):
        error(f"Video file not found: {args.video_path}")
        sys.exit(1)

    # Find account
    accounts = get_accounts("youtube")
    account = None
    for acc in accounts:
        if acc["id"] == args.account_id:
            account = acc
            break

    if account is None:
        error(f"Account not found: {args.account_id}")
        sys.exit(1)

    info(f"Uploading video for account: {account['nickname']}")

    youtube = YouTube(
        account["id"],
        account["nickname"],
        account["firefox_profile"],
        account["niche"],
        account["language"],
    )

    # Set the video path and metadata manually
    youtube.video_path = os.path.abspath(args.video_path)
    youtube.metadata = {"title": args.title, "description": args.description}

    result = youtube.upload_video()

    if result:
        success(f"Upload successful: {youtube.uploaded_video_url}")
        print(f"OUTPUT_VIDEO_URL={youtube.uploaded_video_url}")
    else:
        error("Upload failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

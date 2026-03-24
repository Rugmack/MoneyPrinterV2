#!/usr/bin/env python3
"""Change the visibility of an uploaded YouTube video.

Usage:
    python claude-plugin/scripts/set-video-visibility.py --account-id <UUID> --video-url <url> --visibility unlisted

Must be run from the MoneyPrinterV2 project root.
"""
import argparse
import re
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from cache import get_accounts
from classes.YouTube import YouTube
from constants import YOUTUBE_RADIO_BUTTON_XPATH
from status import success, error, info

VISIBILITY_INDEX = {"public": 0, "private": 1, "unlisted": 2}


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r"youtube\.com/shorts/([a-zA-Z0-9_-]+)",
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)",
        r"youtu\.be/([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def main():
    parser = argparse.ArgumentParser(description="Change YouTube video visibility")
    parser.add_argument("--account-id", required=True, help="YouTube account UUID")
    parser.add_argument("--video-url", required=True, help="YouTube video URL")
    parser.add_argument("--visibility", required=True,
                        choices=["public", "private", "unlisted"],
                        help="Target visibility")
    args = parser.parse_args()

    video_id = extract_video_id(args.video_url)
    if not video_id:
        error(f"Could not extract video ID from URL: {args.video_url}")
        sys.exit(1)

    accounts = get_accounts("youtube")
    account = None
    for acc in accounts:
        if acc["id"] == args.account_id:
            account = acc
            break

    if account is None:
        error(f"Account not found: {args.account_id}")
        sys.exit(1)

    info(f"Changing visibility of {video_id} to {args.visibility}...")

    youtube = YouTube(
        account["id"],
        account["nickname"],
        account["firefox_profile"],
        account["niche"],
        account["language"],
    )

    driver = youtube.browser

    try:
        # Navigate to the video's edit page in YouTube Studio
        youtube.get_channel_id()
        edit_url = f"https://studio.youtube.com/video/{video_id}/edit"
        driver.get(edit_url)
        time.sleep(3)

        # Click "Show more" or navigate to visibility tab
        # In YouTube Studio editor, visibility is under the "Visibility" section
        # We need to find and click the visibility dropdown/section
        from selenium.webdriver.common.by import By

        # Click the visibility button/section in the editor
        # YouTube Studio uses a dropdown for visibility in the edit page
        visibility_button = driver.find_element(
            By.CSS_SELECTOR, "ytcp-video-visibility-select"
        )
        visibility_button.click()
        time.sleep(1)

        # Select the target visibility
        radio_buttons = driver.find_elements(By.XPATH, YOUTUBE_RADIO_BUTTON_XPATH)
        radio_buttons[VISIBILITY_INDEX[args.visibility]].click()
        time.sleep(0.5)

        # Save changes
        save_button = driver.find_element(By.ID, "save-button")
        save_button.click()
        time.sleep(2)

        success(f"Visibility changed to {args.visibility}")
        print(f"OUTPUT_VISIBILITY={args.visibility}")

    except Exception as e:
        error(f"Failed to change visibility: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

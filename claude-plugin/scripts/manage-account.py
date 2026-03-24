#!/usr/bin/env python3
"""Add or remove MPV2 accounts non-interactively.

Usage:
    # Add YouTube account
    python claude-plugin/scripts/manage-account.py add --provider youtube \
        --nickname "My Channel" --firefox-profile /path/to/profile \
        --niche "cooking" --language "English"

    # Add Twitter account
    python claude-plugin/scripts/manage-account.py add --provider twitter \
        --nickname "My Bot" --firefox-profile /path/to/profile \
        --topic "tech news"

    # Remove account
    python claude-plugin/scripts/manage-account.py remove --provider youtube --account-id <UUID>
"""
import argparse
import os
import sys
from uuid import uuid4

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from cache import add_account, remove_account, get_accounts
from config import assert_folder_structure
from status import success, error


def cmd_add(args):
    assert_folder_structure()

    account_id = str(uuid4())

    if args.provider == "youtube":
        if not args.niche or not args.language:
            error("YouTube accounts require --niche and --language")
            sys.exit(1)
        account = {
            "id": account_id,
            "nickname": args.nickname,
            "firefox_profile": args.firefox_profile,
            "niche": args.niche,
            "language": args.language,
            "videos": [],
        }
    elif args.provider == "twitter":
        if not args.topic:
            error("Twitter accounts require --topic")
            sys.exit(1)
        account = {
            "id": account_id,
            "nickname": args.nickname,
            "firefox_profile": args.firefox_profile,
            "topic": args.topic,
            "posts": [],
        }

    add_account(args.provider, account)
    success(f"Account added: {account_id} ({args.nickname})")
    print(f"ACCOUNT_ID={account_id}")


def cmd_remove(args):
    if not args.account_id:
        error("--account-id is required for remove")
        sys.exit(1)

    accounts = get_accounts(args.provider)
    found = any(acc["id"] == args.account_id for acc in accounts)

    if not found:
        error(f"Account not found: {args.account_id}")
        sys.exit(1)

    remove_account(args.provider, args.account_id)
    success(f"Account removed: {args.account_id}")


def main():
    parser = argparse.ArgumentParser(description="Manage MPV2 accounts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new account")
    add_parser.add_argument("--provider", required=True, choices=["youtube", "twitter"])
    add_parser.add_argument("--nickname", required=True)
    add_parser.add_argument("--firefox-profile", required=True)
    add_parser.add_argument("--niche", help="YouTube only: channel niche")
    add_parser.add_argument("--language", help="YouTube only: content language")
    add_parser.add_argument("--topic", help="Twitter only: account topic")

    # Remove command
    rm_parser = subparsers.add_parser("remove", help="Remove an account")
    rm_parser.add_argument("--provider", required=True, choices=["youtube", "twitter"])
    rm_parser.add_argument("--account-id", required=True)

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)


if __name__ == "__main__":
    main()

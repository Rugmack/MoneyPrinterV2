#!/usr/bin/env python3
"""List registered accounts from MPV2 cache.

Usage:
    python claude-plugin/scripts/list-accounts.py --provider youtube
    python claude-plugin/scripts/list-accounts.py --provider twitter
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from cache import get_accounts


def main():
    parser = argparse.ArgumentParser(description="List MPV2 accounts")
    parser.add_argument("--provider", required=True, choices=["youtube", "twitter"])
    args = parser.parse_args()

    accounts = get_accounts(args.provider)

    if not accounts:
        print(f"No {args.provider} accounts found.")
        sys.exit(0)

    for acc in accounts:
        print(json.dumps(acc, indent=2))
        print("---")

    print(f"Total: {len(accounts)} account(s)")


if __name__ == "__main__":
    main()

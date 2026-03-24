#!/usr/bin/env python3
"""List available Ollama models.

Usage:
    python claude-plugin/scripts/list-models.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from llm_provider import list_models
from status import error


def main():
    try:
        models = list_models()
    except Exception as e:
        error(f"Could not connect to Ollama: {e}")
        sys.exit(1)

    if not models:
        print("No models found. Pull a model first: ollama pull llama3.2:3b")
        sys.exit(0)

    for model in models:
        print(model)


if __name__ == "__main__":
    main()

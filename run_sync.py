#!/usr/bin/env python3
"""
Entry point for running the full account sync pipeline.

This script runs the complete pipeline:
1. Generates test visitor signals
2. Enriches them with AI research
3. Syncs the intelligence to Salesforce

Usage:
    python run_sync.py
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from backend.auto_sync import run

if __name__ == "__main__":
    run()

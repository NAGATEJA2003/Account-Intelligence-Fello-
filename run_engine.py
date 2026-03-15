#!/usr/bin/env python3
"""
Entry point for running the AI enrichment engine.

This script processes visitor signals through the AI research agent
to generate account intelligence.

Usage:
    python run_engine.py
"""
from backend.engine import run_engine

if __name__ == "__main__":
    run_engine()

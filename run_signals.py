#!/usr/bin/env python3
"""
Entry point for generating test visitor signals.

This script generates random web traffic signals for testing purposes.

Usage:
    python run_signals.py
"""
from backend.generate_signals import generate_random_traffic

if __name__ == "__main__":
    generate_random_traffic()

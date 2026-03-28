#!/usr/bin/env python3
"""OpenClaw スキル: シチュエーション一覧"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import SITUATIONS

for category, situations in SITUATIONS.items():
    print(f"\n[{category}]")
    for s in situations:
        print(f"  - {s}")

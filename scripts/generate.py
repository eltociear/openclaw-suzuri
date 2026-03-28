#!/usr/bin/env python3
"""OpenClaw スキル: デザイン生成"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from pipeline import run_pipeline

situation = sys.argv[1] if len(sys.argv) > 1 else None
design_id = run_pipeline(situation=situation, upload=True)
print(f"Design created: id={design_id}")

#!/usr/bin/env python3
"""OpenClaw スキル: バッチ生成"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from scheduler import daily_run

count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
daily_run(count=count, upload=True)

#!/usr/bin/env python3
"""OpenClaw スキル: ショップ統計"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import init_db
from analytics import print_report

init_db()
print_report()

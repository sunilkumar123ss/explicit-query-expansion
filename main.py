"""Inspectable one-hop query expansion with exact token-sequence rules."""
import argparse
import json
from pathlib import Path
import re


def tokens(text):return re.findall(r"\w+",text.casefold())


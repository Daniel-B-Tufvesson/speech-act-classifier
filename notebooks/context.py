"""
This code gives import access to the speechact module for the scripts.
Add this to the script: "from context import speechact"
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import speechact
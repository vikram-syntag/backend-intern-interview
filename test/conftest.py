# File: conftest.py
import sys
from pathlib import Path

# Calculate the directory of your application code.
app_dir = Path(__file__).parent.parent / 'app'

# Add the directory to the Python path.
sys.path.insert(0, str(app_dir))

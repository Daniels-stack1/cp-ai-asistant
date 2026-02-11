import sys
import os

# Add the current directory to sys.path to ensure local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import create_app

app = create_app()

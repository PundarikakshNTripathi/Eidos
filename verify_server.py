import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from src import server
    print("Server imported successfully.")
except Exception as e:
    print(f"Failed to import server: {e}")
    sys.exit(1)

"""
Main entry point for Instagram MCP Server.
"""

import os
import sys

# Ensure src directory is in sys.path for local direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from instagram_mcp.server import main

if __name__ == "__main__":
    main()

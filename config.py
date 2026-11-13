# config.py
import os

# Demo user for authorization
DEMO_USER = os.environ.get("DEMO_USER", "demo")
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "demo")

# Basic server settings
HOST = "127.0.0.1"
PORT = 8989

# Logging settings
LOG_LEVEL = "INFO"

# Routing settings
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"

# Operating mode
DEBUG = True

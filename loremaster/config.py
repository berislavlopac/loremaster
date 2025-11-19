from pathlib import Path

import yaml

GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini/gemini-2.5-flash"
# GEMINI_MODEL = "gemini/gemini-2.5-pro"
# GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"
GEMINI_IMAGE_MODEL = "imagen-4.0-generate-001"
DEFAULT_TEMPERATURE = 0.8
DEBUG = True

DEFAULT_TEXT_STYLE = "General style of fantasy novels."
DEFAULT_VISUAL_STYLE = "Hand-drawn sketch in sepia tones."
DEFAULT_PARAGRAPHS = 2

BASE_DIR = Path(__file__).parent
BASE_IMAGES_DIR = BASE_DIR.parent / "images"

AGENTS_CONFIG_FILE = "agents.yaml"

agents = yaml.safe_load((BASE_DIR / AGENTS_CONFIG_FILE).read_text())

from decouple import config
from pathlib import Path

STATIC_URL = config("STATIC_URL", default="static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "media"

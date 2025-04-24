from pathlib import Path
import os

DATA_DIR = str(Path(os.getenv("DATA_DIR", "./data")).resolve())
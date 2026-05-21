import logging
import logging.config
import os
import sys
from pathlib import Path
from pydantic_settings import BaseSettings

# Base directories
ROOT_DIR = Path(__file__).parent.parent.absolute()

class Settings(BaseSettings):
    """Modern configuration management using Pydantic."""
    environment: str = "local"  # e.g., 'local', 'docker', 'prod'
    
    # Default to a local folder, but let Docker override this via environment variables
    # e.g., ENV EFS_DIR=/app/storage in Dockerfile
    efs_dir: Path = ROOT_DIR / "storage" 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure shared storage directories exist (Crucial for Ray/MLflow in Docker)
settings.efs_dir.mkdir(parents=True, exist_ok=True)

# Config MLflow
import mlflow
MODEL_REGISTRY = settings.efs_dir / "mlflow"
MODEL_REGISTRY.mkdir(parents=True, exist_ok=True)
MLFLOW_TRACKING_URI = f"file://{MODEL_REGISTRY.absolute()}"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Docker-ready Logger Setup
# We only use StreamHandler (stdout) when in Docker
handlers = {
    "console": {
        "class": "logging.StreamHandler",
        "stream": sys.stdout,
        "formatter": "detailed",
        "level": logging.INFO,
    }
}

# If running locally, you can optionally add file handlers back in
if settings.environment == "local":
    LOGS_DIR = ROOT_DIR / "logs"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    handlers["file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOGS_DIR / "app.log",
        "maxBytes": 10485760,
        "backupCount": 5,
        "formatter": "detailed",
        "level": logging.INFO,
    }

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
        },
    },
    "handlers": handlers,
    "root": {
        "handlers": list(handlers.keys()),
        "level": logging.INFO,
        "propagate": True,
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Stopwords list remains the same below...

# Stopwords list remains the same (omitted for brevity, but you would keep it here as a native list)
STOPWORDS = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "you're",
    "you've",
    "you'll",
    "you'd",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "she's",
    "her",
    "hers",
    "herself",
    "it",
    "it's",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "that'll",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "don't",
    "should",
    "should've",
    "now",
    "d",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "aren't",
    "couldn",
    "couldn't",
    "didn",
    "didn't",
    "doesn",
    "doesn't",
    "hadn",
    "hadn't",
    "hasn",
    "hasn't",
    "haven",
    "haven't",
    "isn",
    "isn't",
    "ma",
    "mightn",
    "mightn't",
    "mustn",
    "mustn't",
    "needn",
    "needn't",
    "shan",
    "shan't",
    "shouldn",
    "shouldn't",
    "wasn",
    "wasn't",
    "weren",
    "weren't",
    "won",
    "won't",
    "wouldn",
    "wouldn't",
]

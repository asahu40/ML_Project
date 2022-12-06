import os
from datetime import datetime


ROOT_DIR = os.getcwd()  # To Get current Working Directory

CONFIG_DIR = "config"
CONFIG_FILE = "config_yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR , CONFIG_DIR , CONFIG_FILE)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


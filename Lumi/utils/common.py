import os, yaml

from logger import logging
from exception import LumiException

def read_yaml_file(file_path: str) -> dict:
    # try:
    logging.info('[INFO] Reading YAML file')
    with open(file_path, 'rb') as yaml_file:
        return yaml.safe_load(yaml_file)
    # except Exception as e:
    #     logging.error("[ERROR] error occurred while reading YAML file")
    #     raise LumiException(e, sys) from e
import os
from datetime import datetime

from Lumi.constants.eln import *


class Data:
    def __init__(self, timestamp_format = "%m_%d_%Y_%H_%M_%S", timestamp = datetime.now()):
        self.timestamp: str = timestamp.strftime(timestamp_format)
        self.artifact_dir:str = ARTIFACT_DIR
    
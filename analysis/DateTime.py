import time
from datetime import datetime
import ntplib
import os

# TODO : implement controlinand conne

class DateTime:

    def __init__(self, path):
        self.time_modification = os.path.getmtime(path)
        self.time_creation = os.path.getctime(path)
        # global current_time

    def get_time_modification(self):
        return self.time_modification

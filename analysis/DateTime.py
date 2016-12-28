import time
from datetime import datetime
import ntplib
import os

#
# c = ntplib.NTPClient()
# response = c.request('europe.pool.ntp.org', version=3)
# current_time = datetime.strptime(datetime.fromtimestamp(response.tx_time).
#                                  strftime('%a %b %d %H:%M:%S %Y'), "%a %b %d %H:%M:%S %Y")


class DateTime:

    def __init__(self, path):
        self.time_modification = os.path.getmtime(path)
        self.time_creation = os.path.getctime(path)
        # global current_time

    def get_time_modification(self):
        return self.time_modification





import time
from datetime import datetime
import ntplib
import os


c = ntplib.NTPClient()
response = c.request('europe.pool.ntp.org', version=3)
current_time = datetime.strptime(datetime.fromtimestamp(response.tx_time).
                                 strftime('%a %b %d %H:%M:%S %Y'), "%a %b %d %H:%M:%S %Y")


class DateTime:

    def __init__(self, path):
        self.time_modification = datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")
        self.time_creation = datetime.strptime(time.ctime(os.path.getctime(path)), "%a %b %d %H:%M:%S %Y")
        global current_time

    def get_time_modification(self):
        if current_time >= self.time_modification:
            return str(self.time_modification)
        elif self.time_creation <= current_time:
            return str(self.time_creation)





from Block import Block
from File import File
from Folder import Folder
from Logs import Logs
from DateTime import DateTime
import asyncio
import pprint
import pickle
import math
import sys

folder_another = Folder('C:\\Users\\Edward\\Desktop\\test')
folder_my = Folder('C:\\Users\\Edward\\Desktop\\test4')

log_from_another_computer = folder_another.get_log_file()
log_my = folder_my.get_log_file()

result = Logs(log_my, log_from_another_computer).compare()
result2 = Logs(log_from_another_computer, log_my).compare()

folder_my.create(result)
folder_another.create(result2)




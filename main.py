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
from HandlerMessage import HandlerMessage
from Message import Message

folder_another = Folder('C:\\Users\\Edward\\Desktop\\test')
folder_my = Folder('C:\\Users\\Edward\\Desktop\\test4')

msg = Message()

b = HandlerMessage(msg.get_log()).response()

print(b)
log_from_another_computer = b[1]
log_my = folder_my.get_log_file()
result = Logs(log_my, log_from_another_computer).compare()
# result2 = Logs(log_from_another_computer, log_my).compare()

for file_path in result[1]:
    # print(file_path)
    request = msg.get_file(file_path)
    file_obj = log_from_another_computer[file_path]
    file = HandlerMessage(request).response()
    folder_my.create_folders(file_obj.get_rel_path())
    folder_my.create_files(file_obj, file[1])




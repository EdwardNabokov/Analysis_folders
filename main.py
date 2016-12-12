from Block import Block
from File import File
from Folder import Folder
from Logs import Logs
from DateTime import DateTime
import asyncio
import pprint
import pickle
import math


folder1 = Folder('C:\\Users\\Edward\\Desktop\\MKR')
folder2 = Folder('C:\\Users\\Edward\\Desktop\\MKR-2')
folder3 = Folder('C:\\Users\\Edward\\Desktop\\MKR1')
folder4 = Folder('C:\\Users\\Edward\\Desktop\\MKR4')

unmatched_folders = Logs(folder1.get_log_file(), folder2.get_log_file()).compare_folders()
unmatched_files = Logs(folder1.get_log_file(), folder2.get_log_file()).compare()

folder1.create_folder(unmatched_folders)
folder1.create_files(unmatched_files)

unmatched_folders = Logs(folder3.get_log_file(), folder2.get_log_file()).compare_folders()
unmatched_files = Logs(folder3.get_log_file(), folder2.get_log_file()).compare()

folder3.create_folder(unmatched_folders)
folder3.create_files(unmatched_files)

unmatched_folders = Logs(folder4.get_log_file(), folder2.get_log_file()).compare_folders()
unmatched_files = Logs(folder4.get_log_file(), folder2.get_log_file()).compare()

folder4.create_folder(unmatched_folders)
folder4.create_files(unmatched_files)












from Folder import Folder
from File import File
import pprint
import os


class Logs:

    def __init__(self, log_first, log_second):
        self.log_first = log_first
        self.log_second = log_second

    def compare(self):
        absent_files = []
        first_folder = [key for key in self.log_first.keys()]
        second_folder = [key for key in self.log_second.keys()]
        result = set(second_folder) - set(first_folder)
        for each in list(result):
            absent_files.append(list(self.log_second[each])[0])
        return list(absent_files)

    def compare_folders(self):
        absent_folder = []
        for value in self.log_second.values():
            if value not in list(self.log_first.values())[1]:
                absent_folder.append(value[1])
        absent_folder = [value[1] for value in self.log_second.values()]
        return absent_folder
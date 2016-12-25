from Message import Message
from Logs import Logs
import os


class HandlerMessage:

    def __init__(self, info, folder_my, out_queue):
        self.info = info
        self.folder_my = folder_my
        self.out_queue = out_queue
        self.message_response = {
            '__GET_LOG__': self.get_log,
            '__GET_FILE__': self.get_file,
            '__SEND_LOG__': self.send_log,
            '__SEND_FILE__': self.send_file,
            '__CREATE_FILE__': self.create_file,
            '__APPEND_TO_FILE__': self.append_to_file,
        }

    def run(self):
        return self.message_response[self.info[0]]()

    def get_log(self):
        a = Message()
        answer = self.folder_my.get_log_file()
        self.out_queue.put(a.send_log(answer))

    def get_file(self):
        path = self.info[1]
        self.out_queue.put(Message().create_file(self.info[1]))
        with open(self.folder_my.get_file(path).full_path, 'rb') as f:
            data = f.read(1048576)
            self.out_queue.put(Message().append_to_file(path, data))

    def send_log(self):
        different_folders = Logs(self.folder_my.get_log_file(), self.info[1]).cmp_folders()
        different_files = Logs(self.folder_my.get_log_file(), self.info[1]).cmp_files()
        for i in different_folders:
            self.folder_my.create_folder(i)
        for i in different_files:
            self.out_queue.put(Message().get_file(i))

    def send_file(self):
        self.folder_my.create_file(self.info[1], self.info[2])

    def create_file(self):
        self.folder_my.create_file(self.info[1], '')

    def append_to_file(self):
        self.folder_my.append_data(self.info[1], self.info[2])
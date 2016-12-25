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
            '__SEND_FILE__': self.send_file
        }

    def run(self):
        return self.message_response[self.info[0]]()

    def get_log(self):
        a = Message()
        answer = self.folder_my.get_log_file()
        return a.send_log(answer)

    def get_file(self):
        a = Message()
        current_file_path = self.info[1]
        # print('Info: ', self.info)
        current_file_object = self.folder_my.get_file(current_file_path)
        answer = a.send_file(current_file_path, current_file_object.get_file())
        return answer

    def send_log(self):
        difference_folders = Logs(self.folder_my.get_log_file(), self.info[1]).cmp_folders()
        for i in difference_folders:
            # print('Different_folder ', os.path.join(*i))
            self.folder_my.create_folder(i)

        difference_files = Logs(self.folder_my.get_log_file(), self.info[1]).cmp_files()
        msg = Message()
        for i in difference_files:
            # print('I_sdf ', os.path.join(*i))
            self.out_queue.put(msg.get_file(i))
        return None

    def send_file(self):
        # print('Here ', self.info)
        self.folder_my.create_file(self.info[1], self.info[2])
        return None
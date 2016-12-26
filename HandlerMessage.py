from Message import Message
from Logs import Logs


class HandlerMessage:

    def __init__(self, message, folder_my, out_queue):
        self.message = message
        self.folder_my = folder_my
        self.out_queue = out_queue
        self.message_response = {
            '__GET_LOG__': self.get_log,
            '__GET_FILE__': self.get_file,
            '__SEND_LOG__': self.send_log,
            '__CREATE_FILE__': self.create_file,
            '__APPEND_TO_FILE__': self.append_to_file,
        }

    def run(self):
        if self.message.decode_command() in self.message_response.keys():
            return self.message_response[self.message.decode_command()]()

    def get_log(self):
        answer = self.folder_my.get_log_file()
        self.out_queue.put(Message('__SEND_LOG__', answer, ''))

    def get_file(self):
        path = self.message.decode_meta()
        self.out_queue.put(Message('__CREATE_FILE__', self.message.decode_meta(), ''))
        with open(self.folder_my.get_file(path).full_path, 'rb') as f:
            while True:
                data = f.read(10240)
                if data:
                    self.out_queue.put(Message('__APPEND_TO_FILE__', self.message.decode_meta(), data))
                else:
                    break

    def send_log(self):
        different_folders = Logs(self.folder_my.get_log_file(), self.message.decode_meta()).cmp_folders()
        different_files = Logs(self.folder_my.get_log_file(), self.message.decode_meta()).cmp_files()
        for i in different_folders:
            self.folder_my.create_folder(i)
        for i in different_files:
            self.out_queue.put(Message('__GET_FILE__', i, ''))

    def create_file(self):
        self.folder_my.create_file(self.message.decode_meta(), '')

    def append_to_file(self):
        self.folder_my.append_to_file(self.message.decode_meta(), self.message.data)
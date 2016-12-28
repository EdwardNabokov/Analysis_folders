from Message import Message
from analysis.Logs import Logs


class HandlerMessage:

    def __init__(self, message, folder_my, out_queue):
        self.message = message
        self.folder_my = folder_my
        self.out_queue = out_queue
        self.message_response = {
            '__GET_LOG__': self.get_log,
            '__SEND_LOG__': self.send_log,
            '__GET_FILE__': self.get_file,
            '__CREATE_FOLDER__': self.create_folder,
            '__REMOVE_FOLDER__': self.remove_folder,
            '__CREATE_FILE__': self.create_file,
            '__APPEND_TO_FILE__': self.append_to_file,
            '__REMOVE_FILE__': self.remove_file,
            '__MOVE__': self.rename,
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
        try:
            with open(self.folder_my.get_file(path).full_path, 'rb') as f:
                while True:
                    data = f.read(102400)
                    if data:
                        self.out_queue.put(Message('__APPEND_TO_FILE__', self.message.decode_meta(), data))
                    else:
                        break
        except:
            pass

    def send_log(self):
        different_folders = Logs(self.folder_my.get_log_file(), self.message.decode_meta()).cmp_folders()
        different_files = Logs(self.folder_my.get_log_file(), self.message.decode_meta()).cmp_files()
        for i in different_folders:
            self.folder_my.create_folder(i)
        for i in different_files:
            self.out_queue.put(Message('__GET_FILE__', i, ''))

    def create_file(self):
        self.folder_my.create_file(self.message.decode_meta(), '')

    def remove_file(self):
        self.folder_my.remove_file(self.message.decode_meta())

    def append_to_file(self):
        self.folder_my.append_to_file(self.message.decode_meta(), self.message.data)

    def create_folder(self):
        self.folder_my.create_folder(self.message.decode_meta())

    def remove_folder(self):
        self.folder_my.remove_folder(self.message.decode_meta())

    def rename(self):
        path_form, path_to = self.message.decode_meta()
        self.folder_my.rename(path_form, path_to)
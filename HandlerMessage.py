from Message import Message
from Folder import Folder
from Logs import Logs


class HandlerMessage:

    def __init__(self, info, folder_my, out_queue):
        self.info = info
        self.folder_my = folder_my
        self.out_queue = out_queue
        message_response = {
            '__GET_LOG__': self.get_log,
            '__GET_FILE__': self.get_file,
            '__SEND_LOG__': self.send_log,
            '__SEND_FILE__': self.send_file
        }
        message_response[self.info[0]]()

    def get_log(self):
        a = Message()
        answer = self.folder_my.get_log_file()
        return a.send_log(answer)

    def get_file(self):
        a = Message()
        current_file_path = self.info[1]
        current_file_object = self.folder_my.get_file(current_file_path)
        answer = a.send_file(current_file_path, current_file_object.get_file())
        return answer

    def send_log(self):
        difference = Logs(self.folder_my.get_log_file(), self.info[1]).compare()
        self.folder_my.create_folders(difference[0])
        msg = Message()
        for file_path in difference[1]:
            self.out_queue.put(msg.get_file(file_path))
        return None

    def send_file(self):
        print('Here ', self.info[1])
        self.folder_my.create_file(self.info[1], self.info[2])
        return None
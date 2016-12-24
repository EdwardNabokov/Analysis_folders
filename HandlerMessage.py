from Message import Message, commands
from Folder import Folder
from Logs import Logs


class HandlerMessage:

    def __init__(self, info, folder_my):
        self.info = info
        self.folder_my = folder_my

    def response(self):
        if self.info[0] == '__GET_LOG__':
            a = Message()
            answer = self.folder_my.get_log_file()
            return a.send_log(answer)

        if self.info[0] == '__SEND_LOG__':
            a = Message()
            answer = a.got_log(self.info)
            return answer

        if self.info[0] == '__GET_FILE__':
            a = Message()
            current_file_path = self.info[1]
            current_file_object = self.folder_my.get_file(current_file_path)
            answer = a.send_file(current_file_path, current_file_object.get_file())
            return answer

        if self.info[0] == '__SEND_FILE__':
            a = Message()
            current_file_path = self.info[1]
            current_file_object = self.folder_my.get_file(current_file_path)
            answer = a.got_file(current_file_path, current_file_object.get_file())
            return answer
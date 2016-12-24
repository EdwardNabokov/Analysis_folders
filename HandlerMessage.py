from Message import Message, commands
from Folder import Folder
from Logs import Logs

folder_another = Folder('C:\\Users\\Edward\\Desktop\\test')
folder_my = Folder('C:\\Users\\Edward\\Desktop\\test4')


class HandlerMessage:

    def __init__(self, info):
        self.info = info

    def response(self):
        if self.info[0] == '__GET_LOG__':
            a = Message()
            answer = folder_another.get_log_file()
            return a.send_log(answer)

        if self.info[0] == '__SEND_LOG__':
            print('I got your request for log')
            a = Message()
            answer = a.got_log(self.info)
            print(answer)
            return answer

        if self.info[0] == '__GET_FILE__':
            a = Message()
            current_file_path = self.info[1]
            current_file_object = folder_another.get_file(current_file_path)
            answer = a.send_file(current_file_object.get_file())
            return answer

        if self.info[0] == '__SEND_FILE__':
            print('I got your request for file')
            a = Message()
            current = ('__GOT_FILE__', self.info[1])
            answer = a.send_log(current)
            print(answer)
            return answer

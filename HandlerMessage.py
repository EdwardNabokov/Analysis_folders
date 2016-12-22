from Message import Message, commands
from Folder import Folder
from Logs import Logs



folder_another = Folder('C:\\Users\\Edward\\Desktop\\test')
folder_my = Folder('C:\\Users\\Edward\\Desktop\\test4')


class HandlerMessage:

    def __init__(self, info):
        self.info = info

    def get_from(self):
        if self.info[0] == '__GET_LOG__':
            a = Message()
            answer = folder_another.get_log_file()
            return a.send_log(answer)

        if self.info[0] == '__GET_FILE__':
            a = Message()
            print('Info ', self.info)
            current_file_path = self.info[3]
            current_file_object = folder_another.get_file(current_file_path)
            answer = a.send_file(current_file_object.get_file())
            return answer


msg = Message()

b = HandlerMessage(msg.get_log()).get_from()

log_from_another_computer = b[3]
log_my = folder_my.get_log_file()
result = Logs(log_my, log_from_another_computer).compare()
# result2 = Logs(log_from_another_computer, log_my).compare()

for file_path in result[1]:
    # print(file_path)
    request = msg.get_file(file_path)
    file_obj = log_from_another_computer[file_path]
    file = HandlerMessage(request).get_from()
    folder_my.create_folders(file_obj.get_rel_path())
    folder_my.create_files(file_obj, file[3])



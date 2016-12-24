from Folder import Folder
from Message import Message, commands
from HandlerMessage import HandlerMessage
from Logs import *
from queue import *
import time

# folder_another = Folder('C:\\Users\\Edward\\Desktop\\test4')


class Analyzer:

    def __init__(self, path_to_folder, input_queue, output_queue):
        self.path_to_folder = path_to_folder
        self.in_queue = input_queue
        self.out_queue = output_queue
        self.my_log = {}
        self.my_log_copy = {}
        self.another_log = {}
        self.another_log_copy = {}

    def run(self):
        msg = Message()
        folder = Folder(self.path_to_folder)
        self.my_log = folder.get_log_file()

        self.my_log_copy = self.my_log
        self.out_queue.put(msg.get_log())
        # test

        # self.in_queue.put(HandlerMessage(folder_another.get_log_file())

        while True:
            if self.in_queue.empty():
                time.sleep(3)
            else:
                answer = HandlerMessage(self.in_queue.get()).response()
                if answer[0] is not ('__GOT_LOG__' or '__GOT_FILE__'):
                    self.out_queue.put(answer)
                    print('here you are -> ', answer)
                else:
                    self.push_message(answer)
                print(self.out_queue.qsize())

    def push_message(self, answer):
        if answer[0] == '__GOT_LOG__':
            print('Answer: ', answer)
            self.another_log = answer[1]
            print('Another lof', self.another_log)
            print('My log: ', self.my_log)
            if len(self.another_log_copy) == 0:
                self.another_log_copy = self.another_log
                print('It''s new Log folder!')
            diff_files = Logs(self.my_log, self.another_log).compare_files()
            print('Folders: ', diff_files)
            a = Message()
            for i in diff_files:
                request = a.get_file(i)
                self.out_queue.put(request)

        if answer[0] == '__GOT_FILE__':
            print('Got file! utc utc utc')

# msg = Message()
#
# b = Queue()
# b.put(msg.send_log(folder_another.get_log_file()))
# print(msg.send_log(folder_another.get_log_file()))
# print(msg.send_log(Folder('C:\\Users\\Edward\\Desktop\\test').get_log_file()))
# c = Queue()
#
# a = Analyzer('C:\\Users\\Edward\\Desktop\\test', b, c)
# a.run()
#
# print(b.qsize())
# print(c.get())


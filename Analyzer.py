from Folder import Folder
from Message import Message, commands
from HandlerMessage import HandlerMessage
from File import File
from Logs import *
from queue import *
import time

folder_another = Folder('C:\\Users\\Edward\\Desktop\\test4')


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
        self.folder = Folder(self.path_to_folder)
        self.my_log = self.folder.get_log_file()

        self.my_log_copy = self.my_log
        self.out_queue.put(msg.get_log())

        while True:
            if self.in_queue.empty():
                time.sleep(3)
            else:
                # print(self.in_queue.qsize())
                # print('Answer', self.in_queue.get())
                answer = HandlerMessage(self.in_queue.get()).response()
                # print('Answer ->)', answer[0])
                if (answer[0] is not '__GOT_LOG__') and (answer[0] is not '__GOT_FILE__'):
                    self.out_queue.put(answer)
                else:
                    self.push_message(answer)
                # print(self.out_queue.qsize())

    def push_message(self, answer):
        if answer[0] == '__GOT_LOG__':
            self.another_log = answer[1]
            if len(self.another_log_copy) == 0:
                self.another_log_copy = self.another_log
            self.diff_files = Logs(self.my_log, self.another_log).compare()
            # print('LEN(DICT) ->', len(self.diff_files))
            # print('Difference: ', self.diff_files)
            a = Message()
            for rel_path_folder in self.diff_files[0]:
                self.folder.create_folder(rel_path_folder)
            for rel_path_file in self.diff_files[1]:
                request = a.get_file(rel_path_file)
                self.out_queue.put(request)
            # print(self.out_queue.qsize())

        if answer[0] == '__GOT_FILE__':
            # print('Got file! utc utc utc')
            # print(len(answer))
            # for rel_path_file in self.diff_files[1]:
            #     print(rel_path_file)
            #     file_obj = self.another_log[rel_path_file]
            #     print(file_obj)
            #     self.folder.create_files(file_obj, answer[2])
            # self.folder.create_files()
            pass

msg = Message()

b = Queue()
b.put(msg.send_log(folder_another.get_log_file()))


c = Queue()

a = Analyzer('C:\\Users\\Edward\\Desktop\\test', b, c)
a.run()


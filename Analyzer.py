from Folder import Folder
from Message import Message
from File import File
from HandlerMessage import HandlerMessage
from Logs import *
from queue import *
import time


class Analyzer:

    def __init__(self, path_to_folder, input_queue, output_queue):
        self.path_to_folder = path_to_folder
        self.in_queue = input_queue
        self.out_queue = output_queue
        self.my_log = {}
        self.another_log_copy = {}

    def run(self):
        self.folder = Folder(self.path_to_folder)
        self.my_log = self.folder.get_log_file()
        self.out_queue.put(Message('__GET_LOG__', '', ''))
        while True:
            if self.in_queue.empty():
                print('Queue is empty')
                time.sleep(1)
            else:
                answer = HandlerMessage(self.in_queue.get(), self.folder, self.out_queue).run()


if __name__ == '__main__':
    test = File(('', 'TJ.pdf'), 'C:\\Users\\Edward\\Desktop\\test4\\')
    test2 = File(('', 'merged.pdf'), 'C:\\Users\\Edward\\Desktop\\test4\\')
    folder_another = Folder('C:\\Users\\Edward\\Desktop\\test4\\')
    msg = Message()
    b = Queue()
    b.put(msg.send_log(folder_another.get_log_file()))
    b.put(msg.send_file(test.get_rel_path(), test.get_file()))
    b.put(msg.send_file(test2.get_rel_path(), test2.get_file()))
    c = Queue()
    a = Analyzer('C:\\Users\\Edward\\Desktop\\test\\', b, c)
    a.run()


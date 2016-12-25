from Folder import Folder
from Message import Message, commands
from HandlerMessage import HandlerMessage
from File import File
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
        msg = Message()
        self.folder = Folder(self.path_to_folder)
        self.my_log = self.folder.get_log_file()

        self.out_queue.put(msg.get_log())

        while True:
            if self.in_queue.empty():
                time.sleep(3)
            else:
                answer = HandlerMessage(self.in_queue.get(), self.folder, self.out_queue).run()
                if answer is not None:
                    self.out_queue.put(answer)


if __name__ == '__main__':
    test = File('\\', 'C:\\Users\\Edward\\Desktop\\test4\\TJ.pdf')
    test2 = File('\\', 'C:\\Users\\Edward\\Desktop\\test4\\merged.pdf')
    test3 = File('\\', 'C:\\Users\\Edward\\Desktop\\test4\\hehee.txt')
    test4 = File('fromNabokovFILE\\', 'C:\\Users\\Edward\\Desktop\\test4\\fromNabokovFILE\\NabokovTExt.txt')
    folder_another = Folder('C:\\Users\\Edward\\Desktop\\test4')

    msg = Message()
    b = Queue()
    b.put(msg.send_log(folder_another.get_log_file()))
    b.put(msg.send_file(test.get_rel_path_name(), test.get_file()))
    b.put(msg.send_file(test2.get_rel_path_name(), test2.get_file()))
    b.put(msg.send_file(test3.get_rel_path_name(), test3.get_file()))
    b.put(msg.send_file(test4.get_rel_path_name(), test4.get_file()))

    c = Queue()
    a = Analyzer('C:\\Users\\Edward\\Desktop\\test', b, c)
    a.run()


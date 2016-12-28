from queue import Empty
import schedule
import time
from watchdog.observers import Observer
from analysis.HandleChanges import MyHandler

from Message import Message
from analysis.Folder import Folder
from analysis.HandlerMessage import HandlerMessage


class Analyzer:

    def __init__(self, path_to_folder, input_queue, output_queue):
        self.path_to_folder = path_to_folder
        self.in_queue = input_queue
        self.out_queue = output_queue
        self.my_log = {}
        self.another_log_copy = {}

        schedule.every(30).seconds.do(self.test)

    def run(self):
        self.folder = Folder(self.path_to_folder)
        self.my_log = self.folder.get_log_file()
        observer = Observer()
        observer.schedule(MyHandler(self.folder, self.out_queue, self.in_queue), path=self.path_to_folder, recursive=True)
        observer.start()
        self.out_queue.put(Message('__GET_LOG__', '', ''))
        while True:
            if not self.in_queue.empty():
                item = self.in_queue.get()
                HandlerMessage(item, self.folder, self.out_queue).run()
            else:
                schedule.run_pending()

    def test(self):
        self.folder.analyze()
        self.folder.create_log()
        self.out_queue.put(Message('__GET_LOG__', '', ''))


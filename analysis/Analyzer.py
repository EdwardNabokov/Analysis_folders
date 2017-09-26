# import basic libraries
import time
from queue import Empty
import schedule
from watchdog.observers import Observer

# import custom modules
from network.Message import Message
from analysis.Folder import Folder
from analysis.HandleChanges import MyHandler
from analysis.HandlerMessage import HandlerMessage


class Analyzer:
    def __init__(self, path_to_folder, input_queue, output_queue):
        """
        Base constructor for Analyzer.

        Parameters
        ----------
        path_to_folder : str
            It's the path to folder, that will be analyzed.

        input_queue : janus.Queue(loop)
            This queue is used for receiving input messages.

        output_queue : janus.Queue(loop)
            This queue is used for sending output messages.

        Variables
        ---------
        my_log : dict
            Here will be kept the structure of folder, that will be analyzed.
            The structure is supposed to be a relationship between each file
            and folder, which it belongs to.

        another_log_copy : dict
            This is a deep copy of my_log.

        """

        self.path_to_folder = path_to_folder
        self.in_queue = input_queue
        self.out_queue = output_queue
        self.my_log = {}
        self.another_log_copy = {}

        # it detects realtime changes in both folders
        schedule.every(30).seconds.do(self.test)

    def run(self):
        """
        It is the main process, which analyzes folder according to
        the path to folder, and creates log file of its content.
        Moreover, it starts observer, which detects changes
        (e.g create/delete folder/file, change folder/file).

        """

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
        """Runs analyzer of the folder, and creates log of it."""

        self.folder.analyze()
        self.folder.create_log()
        self.out_queue.put(Message('__GET_LOG__', '', ''))

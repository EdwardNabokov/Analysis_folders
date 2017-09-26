# import basic libraries
import os
from threading import Timer
from watchdog.events import FileSystemEventHandler

# import custom modules
from network.Message import Message
from analysis.File import File


class MyHandler(FileSystemEventHandler):
    def __init__(self, folder, out_queue, in_queue):
        """
        Base constructor for Handler.

        Parameters
        ----------
        folder : Folder
            It's folder, that is being analyzed.

        out_queue : janus.Queue()
            Get output requests.

        in_queue : janus.Queue()
            It's used for sending responses.

        """

        super(MyHandler, self).__init__()
        self.folder = folder
        self.out_queue = out_queue
        self.in_queue = in_queue

    def on_moved(self, event):
        """Act, when moved file was detected."""
        path_from = tuple(event.src_path[len(self.folder.base_path):].split(os.path.sep))
        path_to = tuple(event.dest_path[len(self.folder.base_path):].split(os.path.sep))
        self.out_queue.put(Message('__MOVE__', (path_from, path_to), b''))

    # TODO : implement action, when file is being modified.
    def on_modified(self, event):
        pass

    def on_created(self, event):
        """Act, when created file was detected."""
        path = tuple(event.src_path[len(self.folder.base_path):].split(os.path.sep))
        if '.' in path[-1]:
            try:
                self.folder.files.append(File(path, self.folder.base_path))
                delay = Timer(3, lambda: self.in_queue.put(Message('__GET_FILE__', path, b'')))
                delay.start()
            except:
                pass
        else:
            self.out_queue.put(Message('__CREATE_FOLDER__', path, b''))

    def on_deleted(self, event):
        """Act, when deleted file was detected."""
        path = tuple(event.src_path[len(self.folder.base_path):].split(os.path.sep))
        if '.' in path[-1]:
            self.folder.remove_file(path)
            self.out_queue.put(Message('__REMOVE_FILE__', path, b''))
        else:
            self.folder.remove_folder(path)
            self.out_queue.put(Message('__REMOVE_FOLDER__', path, b''))

from watchdog.events import FileSystemEventHandler
import os
from Message import Message
from analysis.File import File
from threading import Timer


class MyHandler(FileSystemEventHandler):

    def __init__(self, folder, out_queue, in_queue):
        super(MyHandler, self).__init__()
        self.folder = folder
        self.out_queue = out_queue
        self.in_queue = in_queue

    def on_moved(self, event):
        path_from = tuple(event.src_path[len(self.folder.base_path):].split(os.path.sep))
        path_to = tuple(event.dest_path[len(self.folder.base_path):].split(os.path.sep))
        self.out_queue.put(Message('__MOVE__', (path_from, path_to), b''))

    def on_modified(self, event):
        pass

    def on_created(self, event):
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
        path = tuple(event.src_path[len(self.folder.base_path):].split(os.path.sep))
        if '.' in path[-1]:
            self.folder.remove_file(path)
            self.out_queue.put(Message('__REMOVE_FILE__', path, b''))
        else:
            self.folder.remove_folder(path)
            self.out_queue.put(Message('__REMOVE_FOLDER__', path, b''))
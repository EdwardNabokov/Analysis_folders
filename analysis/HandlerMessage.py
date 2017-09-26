# import custom modules
from network.Message import Message
from analysis.Logs import Logs


class HandlerMessage:

    def __init__(self, message, obj_Folder, out_queue):
        """
        Base constructor for handler messages.

        Parameters
        ----------
        message : str
            Command that is required to handle.

        obj_Folder : Folder
            Object of Folder.

        out_queue : janus.Queue()
            Is used to send responses.

        """

        self.message = message
        self.obj_Folder = obj_Folder
        self.out_queue = out_queue
        self.message_response = {
            '__GET_LOG__': self.get_log,
            '__SEND_LOG__': self.send_log,
            '__GET_FILE__': self.get_file,
            '__CREATE_FOLDER__': self.create_folder,
            '__REMOVE_FOLDER__': self.remove_folder,
            '__CREATE_FILE__': self.create_file,
            '__APPEND_TO_FILE__': self.append_to_file,
            '__REMOVE_FILE__': self.remove_file,
            '__MOVE__': self.rename,
        }

    def run(self):
        """Decode command and return response on it."""
        if self.message.decode_command() in self.message_response.keys():
            return self.message_response[self.message.decode_command()]()

    def get_log(self):
        """Send log as response."""
        answer = self.obj_Folder.get_log_file()
        self.out_queue.put(Message('__SEND_LOG__', answer, ''))

    def get_file(self):
        """Send file as response."""
        path = self.message.decode_meta()
        self.out_queue.put(Message('__CREATE_FILE__', self.message.decode_meta(), ''))
        try:
            with open(self.obj_Folder.get_file(path).full_path, 'rb') as f:
                while True:
                    data = f.read(102400)
                    if data:
                        self.out_queue.put(Message('__APPEND_TO_FILE__', self.message.decode_meta(), data))
                    else:
                        break
        except:
            pass

    def send_log(self):
        """Request for a file."""
        compare = Logs(self.obj_Folder.get_log_file(), self.message.decode_meta())
        different_folders = compare.cmp_folders()
        different_files = compare.cmp_files()
        equal_files = compare.equal_files()

        for i in different_folders:
            self.obj_Folder.create_folder(i)
        for i in different_files:
            self.out_queue.put(Message('__GET_FILE__', i, ''))
        for i in equal_files:
            if i[1]:
                print('*' * 30)
                print('old file', i)
                print('*' * 30)
                self.out_queue.put(Message('__GET_FILE__', i[0], ''))

    def create_file(self):
        self.obj_Folder.create_file(self.message.decode_meta(), '')

    def remove_file(self):
        self.obj_Folder.remove_file(self.message.decode_meta())

    def append_to_file(self):
        self.obj_Folder.append_to_file(self.message.decode_meta(), self.message.data)

    def create_folder(self):
        self.obj_Folder.create_folder(self.message.decode_meta())

    def remove_folder(self):
        self.obj_Folder.remove_folder(self.message.decode_meta())

    def rename(self):
        path_form, path_to = self.message.decode_meta()
        self.obj_Folder.rename(path_form, path_to)

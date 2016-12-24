import os
import sys
from File import File
from sys import platform


class Folder:

    def __init__(self, path, size_of_block=1024):
        """
        initialize essential parameters
        :param path: path to current folder
        :param size_of_block: 1024 by default
        """
        self.base_path = path
        self.log_file = {}
        self.folder_name = os.path.basename(self.base_path)
        self.key = ''
        for root, directories, files in os.walk(self.base_path):
            for file in files:
                if len(self.base_path) == len(root):
                    rel_path = '\\'
                    key = rel_path + file
                else:
                    rel_path = root[len(self.base_path):]
                    key = rel_path + '\\' + file
                if platform != 'Win32':
                    key = key.replace('\\', '/')
                    rel_path = rel_path.replace('\\', '/')
                else:
                    key = key.replace('/', '\\')
                    rel_path = rel_path.replace('/', '\\')

                self.log_file[key] = File(rel_path, self.base_path + key)

    def get_log_file(self):
        return self.log_file

    def get_file(self, path_to_file):
        return self.log_file[path_to_file]

    def get_path(self):
        return self.base_path

    def create_folder(self, path_to_folder):
        """
        create folder in the current path to folder
        :param path_to_folder: it's path to the current folder
        """
        try:
            if not os.path.exists(self.base_path + path_to_folder):
                os.makedirs(self.base_path + path_to_folder)
                print("Created!")
        except:
            print("Something went wrong!")
            sys.exit(0)

    def create_files(self, file_object, file):
        """
        create files in the current directory
        :param file_object: certain file that we have to create
        :param file: file (in bytes)
        """
        try:

            print('file_object.get_file_path() ->', file_object.get_file_path())
            curr_path = self.base_path + '\\' + file_object.get_file_path()

            if platform != 'Win32':
                curr_path = curr_path.replace('\\', '/')
            else:
                curr_path = curr_path.replace('/', '\\')

            f = open(curr_path, 'wb+')
            f.write(file)
            f.close()
            if os.path.exists(file_object.get_file_path()):
                print('created')
        except:
            print("Files weren't delivered")
            sys.exit(0)

    def create(self, folders_an_files):
        self.create_folder(folders_an_files[0])
        # self.create_files(folders_an_files[1], )

folder_another = Folder('C:\\Users\\Edward\\Desktop\\test4')
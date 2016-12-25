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
        self.log_folder = {}
        self.log_folder_copy = {}
        self.folder_name = os.path.basename(self.base_path)
        self.key = ''
        for root, directories, files in os.walk(self.base_path):
            for file in files:
                if file[0] == '.':
                    continue
                rel_folder = [self.folder_name] + root[len(self.base_path):].split(os.sep)[1:]
                rel_folder.append(file)
                print('ww ',os.sep + os.path.join(*rel_folder[1:]))
                self.log_folder[os.path.join(*(rel_folder[1:]))] = File(os.path.join(*rel_folder[1:]), root + os.sep + file)
        print('MY_LOOOOG -> ', self.log_folder)

    def put_log_folder(self, log):
        self.log_folder = log

    def put_log_folder_copy(self, log_copy):
        self.log_folder_copy = log_copy

    def get_log_file(self):
        return self.log_folder

    def get_file(self, path_to_file):
        return self.log_folder[path_to_file]

    def get_path(self):
        return self.base_path

    def create_folders(self, path_to_folders):
        """
        create folder in the current path to folder
        :param path_to_folder: it's path to the current folder
        """
        try:
            for path_to_folder in path_to_folders:
                print('Path to folder: ', path_to_folder)

                if not os.path.exists(self.base_path + path_to_folder):
                    os.makedirs(self.base_path + path_to_folder)
                    print("Created!")
        except:
            print("Something went wrong!")
            sys.exit(0)

    def create_file(self, rel_file_path, file):
        """
        create files in the current directory
        :param file_object: certain file that we have to create
        :param file: file (in bytes)
        """
        try:
            # print('file_object.get_file_path() ->', rel_file_path)

            if platform != 'win32':
                rel_file_path = rel_file_path.replace('\\', '/')
                cur_path = self.base_path + rel_file_path[1:]
            else:
                rel_file_path = rel_file_path.replace('/', '\\')
                cur_path = self.base_path + rel_file_path
            f = open(cur_path, 'wb+')
            f.write(file)
            f.close()
            if os.path.exists(rel_file_path):
                print('created')
        except:
            print("Files weren't delivered")
            sys.exit(0)

    def create(self, folders_an_files):
        self.create_folders(folders_an_files[0])
        # self.create_files(folders_an_files[1], )

#Folder('C:\\Users\\Edward\\Desktop\\test4\\')
import os
import sys
from File import File
import pickle
import io


class Folder:

    def __init__(self, path, size_of_block=256):
        # List which will store all of the full file_paths.
        self.base_path = path
        self.log_file = {}
        self.p = os.path.basename(self.base_path)
        self.key = ''
        for root, directories, files in os.walk(self.base_path):
            for file in files:
                if len(self.base_path) == len(root):
                    rel_path = '\\'
                    key = rel_path + file
                else:
                    rel_path = root[len(self.base_path):]
                    key = rel_path + '\\' + file
                self.log_file[key] = [File(rel_path, self.base_path + key), rel_path]

    def get_log_file(self):
        return self.log_file

    def get_info_of_file(self, path_file):
        return self.log_file[name_file]

    def get_file(self, path_to_file):
        return self.log_file[path_to_file]

    def get_path(self):
        return self.base_path

    def create_folder(self, path_to_folders):
        try:
            for item in path_to_folders:
                if not os.path.exists(self.base_path + item):
                    os.makedirs(self.base_path + item) # here
                    print("Created!")
        except:
            print("Something went wrong!")
            sys.exit(0)

    def create_files(self, file_objects):
        try:
            for file in file_objects:
                print(file)
                f = open(self.base_path + file.get_file_path(), 'wb+')
                f.write(file.get_file())
                f.close()
                if os.path.exists(file.get_file_path()):
                    print('created')
        except:
            print("Files weren't delivered")
            sys.exit(0)



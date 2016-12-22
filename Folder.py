import os
import sys
from File import File


class Folder:

    def __init__(self, path, size_of_block=1024):
        # List which will store all of the full file_paths.
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
                self.log_file[key] = File(rel_path, self.base_path + key)

    def get_log_file(self):
        return self.log_file

    def get_file(self, path_to_file):
        return self.log_file[path_to_file]

    def get_path(self):
        return self.base_path

    def create_folders(self, path_to_folder):
        try:

            if not os.path.exists(self.base_path + path_to_folder):
                os.makedirs(self.base_path + path_to_folder) # here
                print("Created!")
        except:
            print("Something went wrong!")
            sys.exit(0)

    def create_files(self, file_object, file):
        try:
            f = open(self.base_path + '\\' + file_object.get_file_path(), 'wb+')
            f.write(file)
            f.close()
            if os.path.exists(file_object.get_file_path()):
                print('created')
        except:
            print("Files weren't delivered")
            sys.exit(0)

    def create(self, folders_an_files):
        self.create_folders(folders_an_files[0])
        # self.create_files(folders_an_files[1], )




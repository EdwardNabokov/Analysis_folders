import os
import sys
import copy
import shutil
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
        self.log_new = {}
        self.log_old = {}
        self.folders = []
        self.files = []
        self.analyze()
        self.create_log()

    def analyze(self):
        for root, directories, ifiles in os.walk(self.base_path):
            for dir in directories:
                self.folders.append(tuple(os.path.join(root[len(self.base_path):], dir).split(os.sep)))
            for file in ifiles:
               self.files.append(File(tuple(os.path.join(root[len(self.base_path):], file).split(os.sep)), self.base_path))

    def create_log(self):
        self.log_old = copy.deepcopy(self.log_new)
        self.log_new['folders'] = copy.deepcopy(self.folders)
        self.log_new['files'] = copy.deepcopy(self.files)

    def get_log_file(self):
        return self.log_new

    def get_file(self, path_to_file):
        for x in self.files:
            if x.get_rel_path() == path_to_file:
                return x
        return None

    def get_path(self):
        return self.base_path

    def create_folder(self, path_to_folder):
        """
        create folder in the current path to folder
        :param path_to_folder: it's path to the current folder
        """
        try:
            a = []
            for folder in path_to_folder:
                a.append(folder)
                if tuple(a) not in self.folders:
                    os.makedirs(self.base_path + os.path.join(*a))
                    self.folders.append(a)
                    print("Created!")
        except:
            print("Something went wrong!")

    def remove_folder(self, path_to_folder):
        self.folders = [x for x in self.folders if os.path.join(*path_to_folder) not in os.path.join(*x)]
        try:
            shutil.rmtree(os.path.join(self.base_path, *path_to_folder))
        except:
            pass

    def create_file(self, rel_file_path, file):
        """
        create files in the current directory
        :param file_object: certain file that we have to create
        :param file: file (in bytes)
        """
        try:
            self.create_folder(rel_file_path[:-1])
            with open(os.path.join(self.base_path, *rel_file_path), 'wb+') as f:
                f.write(file)
            self.files.append(File(rel_file_path, self.base_path))
            if not os.path.exists(self.base_path + os.path.join(*rel_file_path)):
                print('Error while creating file')
        except:
            print("Files weren't delivered")

    def remove_file(self, path_to_file):
        try:
            os.remove(os.path.join(self.base_path, *path_to_file))
            for i, x in enumerate(self.files):
                if x.get_rel_path() == path_to_file:
                    del self.files[i]
                    break
        except:
            pass



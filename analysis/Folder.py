# import basic libraries
import copy
import os
import shutil

# import custom modules
from analysis.File import File


class Folder:
    def __init__(self, path, size_of_block=1024):
        """
        Base constructor for Folder object.

        Parameters
        ----------
        path : str
            Path to the current folder.

        size_of_block : int (defulat 1024)
            Size of block. Future files of the current folder will be splitted
            by this size.

        Variables
        ---------
        log_new : dict
            Keeps structure of the current folder.

        folders : list
            Keeps all accommodated folders.

        files : list
            Keeps all accommodated files.

        """

        self.base_path = path
        self.log_new = {}
        self.folders = []
        self.files = []

        # call an analyzer for this folder
        self.analyze()

        # call to create log (structure) of this folder
        self.create_log()

    def analyze(self):
        """
        Analyze folder. Search for directories and files.
        Omit (skip) invisible files, that start with dot.

        """

        self.folders = []
        self.files = []
        for root, directories, ifiles in os.walk(self.base_path):
            for dir in directories:
                self.folders.append(tuple(os.path.join(root[len(self.base_path):], dir).split(os.sep)))
            for file in ifiles:
               if file[0] == '.':
                   continue
               self.files.append(File(tuple(os.path.join(root[len(self.base_path):], file).split(os.sep)), self.base_path))

    def create_log(self):
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
        Create folder in the current path to folder.

        Parameters
        ----------
        path_to_folder : path
            It's path to the current folder.

        """

        a = []
        for folder in path_to_folder:
            a.append(folder)
            if tuple(a) not in self.folders:
                try:
                    os.makedirs(self.base_path + os.path.join(*a))
                except:
                    pass
                self.folders.append(a)

    def remove_folder(self, path_to_folder):
        """
        Remove folder in the current path to folder.

        Parameters
        ----------
        path_to_folder : path
            It's path to the current folder.

        """

        self.folders = [x for x in self.folders if os.path.join(*path_to_folder) not in os.path.join(*x)]
        try:
            shutil.rmtree(os.path.join(self.base_path, *path_to_folder))
        except:
            pass

    def create_file(self, rel_file_path, file):
        """
        Create file in the current directory.

        Parameters
        ----------
        rel_file_path : path
            It's path to the current folder.

        file : bytes
            Content of the file.

        """

        if len(rel_file_path) > 2:
            self.create_folder(rel_file_path[:-1])
        try:
            with open(os.path.join(self.base_path, *rel_file_path), 'wb+') as f:
                f.write(file)

            if rel_file_path not in [x.get_rel_path() for x in self.files]:
                self.files.append(File(rel_file_path, self.base_path))
            if not os.path.exists(self.base_path + os.path.join(*rel_file_path)):
                print('Error while creating file')
        except:
            pass

    def remove_file(self, path_to_file):
        """
        Remove file from the current directory.

        Parameters
        ----------
        path_to_file : path
            It's path to the current file.

        """

        for i, x in enumerate(self.files):
            if x.get_rel_path() == path_to_file:
                try:
                    del self.files[i]
                except:
                    break
        try:
            os.remove(os.path.join(self.base_path, *path_to_file))
        except:
            pass

    def append_to_file(self, path, data):
        """
        Append to the exist file new information.

        Parameters
        ----------
        path : list
            Path to the file.

        data : bytes
            Desired information to append.

        """

        try:
            with open(os.path.join(self.base_path, *path), 'ab') as f:
                f.write(data)
        except:
            self.create_file(path)
            with open(os.path.join(self.base_path, *path), 'ab') as f:
                f.write(data)

    def rename(self, path_from, path_to):
        """
        Rename file.

        Parameters
        ----------
        path_from : list
            It's old name of the file.

        path_to : list
            It's new name of the file.

        """

        try:
            shutil.move(os.path.join(self.base_path, *path_from), os.path.join(self.base_path, *path_to))
        except:
            pass

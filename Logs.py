class Logs:

    def __init__(self, log_first, log_second):
        self.log_first = log_first
        self.log_second = log_second

    def cmp_folders(self):
        set_my_folders = set(self.log_first['folders'])
        set_other_folders = set(self.log_second['folders'])

        different_folders = set_other_folders - set_my_folders

        print('Different_folders: ', different_folders)
        return list(different_folders)

    def cmp_files(self):
        set_my_files = set([x.get_rel_path() for x in self.log_first['files']])
        set_other_files = set([x.get_rel_path() for x in self.log_second['files']])

        different_files = set_other_files - set_my_files

        print('Different_files: ', different_files)
        return list(different_files)
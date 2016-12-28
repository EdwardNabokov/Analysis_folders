class Logs:

    def __init__(self, log_first, log_second):
        self.log_first = log_first
        self.log_second = log_second

    def cmp_folders(self):
        set_my_folders = set(self.log_first['folders'])
        set_other_folders = set(self.log_second['folders'])

        different_folders = set_other_folders - set_my_folders

        # print('Different_folders: ', different_folders)
        return list(different_folders)

    def cmp_files(self):
        set_my_files = set([x.get_rel_path() for x in self.log_first['files']])
        set_other_files = set([x.get_rel_path() for x in self.log_second['files']])

        different_files = set_other_files - set_my_files
        return list(different_files)

    def equal_files(self):
        my = []
        other = []
        set_my_files = set([x.get_rel_path() for x in self.log_first['files']])
        set_other_files = set([x.get_rel_path() for x in self.log_second['files']])
        set_equal = set_my_files & set_other_files
        for x in set_equal:
            for my_file in self.log_first['files']:
                if x == my_file.get_rel_path():
                    my.append(my_file)
                    break

            for other_file in self.log_second['files']:
                if x == other_file.get_rel_path():
                    other.append(other_file)

        out = []
        for x in range(len(my)):
            if (my[x].time_of_modification < other[x].time_of_modification):
                out.append((my[x].get_rel_path(), True))
            else:
                out.append((my[x].get_rel_path(), False))
        return out
class Logs:

    def __init__(self, log_first, log_second):
        self.log_first = log_first
        self.log_second = log_second

    def compare_files(self):
        absent_files = []
        first_set = [key for key in self.log_first.keys()]
        second_set = [key for key in self.log_second.keys()]
        result = set(second_set) - set(first_set)
        result2 = set(second_set) & set(first_set)
        for each in list(result):
            absent_files.append(each)
        if len(absent_files) == 0:
            pass
            # print('There is no files to download')
        print(result2)
        for key_path in list(result2):
            if self.log_first[key_path] == self.log_second[key_path]:
                print('Equal?')
        # absent_files = [key for key in self.log_second.keys()]
        return sorted(absent_files)

    def compare_folders(self):
        first_set = [value.get_rel_path() for value in self.log_first.values()]
        second_set = [value.get_rel_path() for value in self.log_second.values()]
        absent_folders_paths = set(second_set) - set(first_set)
        # absent_folder = [value[1] for value in self.log_second.values()]
        if len(absent_folders_paths) == 0 and len(self.log_second.values()) == 0:
            absent_folders_paths = [value.get_rel_path() for value in self.log_first.values()]
        absent_folders_paths = list(absent_folders_paths)
        return sorted(absent_folders_paths)

    def compare(self):
        return self.compare_folders(), self.compare_files()

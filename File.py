from Block import Block
from DateTime import DateTime
import os
import math
from sys import platform


class File:

    def __init__(self, rel_path, file_path, block_size=1024):
        """
        initialize essential parameters
        :param rel_path: it's path EXACTLY from the current folder (Example: ..//test)
        :param file_path: it's path from its root (Example: C://Downloads//test)
        :param block_size: 1024 by default
        """
        self.block_size = block_size
        self.file_path = file_path
        self.rel_path = rel_path
        self.file_name = os.path.basename(file_path)
        self.size_of_file = os.path.getsize(self.file_path)
        self.amount_of_blocks = self.size_of_file / self.block_size
        self.time_of_modification = DateTime(self.file_path).get_time_modification()
        self.list_blocks_checksums = [value.simple_checksum for i, value in enumerate(self._iterator_block_list())]

    def __eq__(self, other):
        if len(self.list_blocks_checksums) < len(other.list_blocks_checksums):
            for i, checksum in enumerate(self.list_blocks_checksums):
                if self._iterator_block_list() == other.list_blocks_checksums[i]:
                    # print('qwe equal')
                    pass
                    #print('Block with position {} are different'.format(i))
        else:
            for i, checksum in enumerate(other.list_blocks_checksums):
                if checksum != self.list_blocks_checksums[i]:
                    pass
                    #print('Block with position {} are different'.format(i))

    def file_name(self):
        return self.file_name

    def get_file_path(self):
        curr_path = self.file_path
        return curr_path

    def get_list_checksums(self):
        pass

    def get_file_name(self):
        return self.file_name

    def get_rel_path_name(self):
        curr_path = self.rel_path + os.sep + self.file_name
        return curr_path

    def get_rel_path(self):
        return self.rel_path

    def get_block_size(self):
        return self.block_size

    def get_size_of_file(self):
        return self.size_of_file

    def get_time_modification(self):
        """
        Get date of last modification
        :return: time of last modification
        """
        return self.time_of_modification

    def get_amount_of_blocks(self):
        return self.amount_of_blocks

    def get_sums_each_block(self):
        list_check = []
        block = self._iterator_block_list()
        for x in range(math.ceil(self.amount_of_blocks)):
            list_check.append(next(block).simple_checksum)
        return list_check

    # def get_unmatched_blocks(self, list_check_sums):
    #     """
    #     Find unmatched blocks
    #     :param list_check_sums: list of check sums from another computer (list(int))
    #     :return: list of unmatched blocks (Block)
    #     """
    #     list_unmatched = []
    #     for i, iter_ch_sum in enumerate(self._iterator_block_list()):
    #         if iter_ch_sum != list_check_sums[i]:
    #             list_unmatched.append(iter_ch_sum)
    #     return list_unmatched

    def _iterator_block_list(self):
        """
        iterate blocks in file
        :return: block
        """
        i = 0
        with open(self.file_path, 'rb') as file:
            block = Block(i, file.read(self.block_size))
            while block.get_block() != b'':
                yield block
                i += 1
                block = Block(i, file.read(self.block_size))

    def get_file(self):
        with open(self.file_path, 'rb') as opened:
                return bytes(opened.read())
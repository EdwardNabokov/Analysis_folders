from Block import Block
from DateTime import DateTime
import os
import math


class File:

    def __init__(self, rel_path, file_path, block_size=1):
        self.block_size = block_size
        self.file_path = file_path
        self.rel_path = rel_path
        self.file_name = os.path.basename(file_path)
        self.size_of_file = os.path.getsize(self.file_path)
        self.amount_of_blocks = self.size_of_file / self.block_size
        self.time_of_modification = DateTime(self.file_path).get_time_modification()

    def file_name(self):
        return self.file_name

    def get_file_path(self):
        return self.rel_path + '\\' + self.file_name

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

    def get_unmatched_blocks(self, list_check_sums):
        """
        Find unmatched blocks
        :param list_check_sums: list of check sums from another computer (list(int))
        :return: list of unmatched blocks (Block)
        """
        list_unmatched = []
        for i, iter_ch_sum in enumerate(self._iterator_block_list()):
            if iter_ch_sum != list_check_sums[i]:
                list_unmatched.append(iter_ch_sum)

        return list_unmatched

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
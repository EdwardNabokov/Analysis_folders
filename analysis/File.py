# import basic libraries
import math
import os

# import custom modules
from analysis.Block import Block
from analysis.DateTime import DateTime


class File:
    def __init__(self, rel_path, file_base, block_size=1024):
        """
        Base constructor for File object.

        Parameters
        ----------
        rel_path : tuple( folder[,folder], file_name )
            It keeps relative path from give path to folder, that is being
            analyzing and its child (e.g folders, files).

        file_path : path
            It's path from its root (e.g C://Downloads/test).

        block_size : int (default 1024)
            Size of the block.

        """

        self.block_size = block_size
        self.file_base = file_base
        self.rel_path = rel_path
        self.file_name = self.rel_path[-1]
        self.full_path = os.path.join(self.file_base, *self.rel_path)
        self.size_of_file = os.path.getsize(self.full_path)
        self.amount_of_blocks = self.size_of_file / self.block_size
        self.time_of_modification = DateTime(self.full_path).get_time_modification()
        self.list_blocks_checksums = [value.simple_checksum for i, value in enumerate(self._iterator_block_list())]


    # TODO : implement comparison two files splitting them on blocks.
    def __eq__(self, other):
        if len(self.list_blocks_checksums) < len(other.list_blocks_checksums):
            for i, checksum in enumerate(self.list_blocks_checksums):
                if self._iterator_block_list() == other.list_blocks_checksums[i]:
                    pass
        else:
            for i, checksum in enumerate(other.list_blocks_checksums):
                if checksum != self.list_blocks_checksums[i]:
                    pass

    def get_file_name(self):
        return self.file_name

    def get_rel_path(self):
        return self.rel_path

    def get_block_size(self):
        """Return default size of block."""
        return self.block_size

    def get_size_of_file(self):
        """Return size of the file."""
        return self.size_of_file

    def get_time_modification(self):
        """Return last time of file's modification."""
        return self.time_of_modification

    def get_amount_of_blocks(self):
        """Return amount of blocks in file."""
        return self.amount_of_blocks

    def get_sums_each_block(self):
        """Split file on blocks, compute their checksums and add them to list."""
        list_check = []
        block = self._iterator_block_list()
        for x in range(math.ceil(self.amount_of_blocks)):
            list_check.append(next(block).simple_checksum)
        return list_check

    def _iterator_block_list(self):
        """Iterate through each block in file."""
        i = 0
        with open(self.full_path, 'rb') as file:
            block = Block(i, file.read(self.block_size))
            while block.get_block() != b'':
                yield block
                i += 1
                block = Block(i, file.read(self.block_size))

    def get_file(self):
        """Generator for each new file."""
        with open(self.full_path, 'rb') as opened:
            for line in opened:
                yield line

    def __repr__(self):
        return str(self.rel_path)

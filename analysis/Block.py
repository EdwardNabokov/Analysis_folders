# import basic libraries
import hashlib
import asyncio
import time
import zlib


class Block:
    def __init__(self, position, block):
        """
        Base constructor for block in a file.

        Parameters
        ----------
        position : int
            It is a position in a file of certain block.

        block : bytes
            It is a content of the block.

        Variables
        ---------
        simple_checksum : hash
            It is an simple checksum that is used in rsync.
            There is also hard checksum.

        """

        self.position = position
        self.block = block
        self.simple_checksum = self.get_simple_checksum()

    def get_position(self):
        return self.position

    # TODO : implement weak checksum
    def __weak_check_sum(data):
        pass

    def get_simple_checksum(self):
        # compute and return simple checksum for block
        return zlib.adler32(self.block)

    def get_hard_checksum(self):
        # compute and return hard checksum for block
        return hashlib.md5(self.block).hexdigest()

    def get_block(self):
        # return block's content
        return self.block

    def __eq__(self, other_check_sum):
        return self.simple_checksum == other_check_sum

    def __str__(self):
        return str(self.block)

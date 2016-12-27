import hashlib
import asyncio
import time
import zlib


class Block:

    def __init__(self, position, block):
        self.position = position
        self.block = block
        self.simple_checksum = self.get_simple_checksum()

    def get_position(self):
        return self.position

    # @staticmethod
    # def __weak_check_sum(data):
    #     """
    #     Generates a weak checksum from an iterable set of bytes.
    #     """
    #     a = b = 0
    #     for i in range(len(data)):
    #         a += data[i]
    #         b += (len(data) - i + 1) * data[i]
    #     a %= 2 ** 16
    #     b %= 2 ** 16
    #     return (b << 16) + a

    def get_simple_checksum(self):
        # hash_w = self.weak_check_sum(bytes(self.block))
        hash_w = zlib.adler32(self.block)
        return hash_w

    def get_hard_checksum(self):
        hash_s = hashlib.md5(self.block).hexdigest()
        return hash_s

    def get_block(self):
        return self.block

    def __eq__(self, other_check_sum):
        # print('comparing')
        return self.simple_checksum == other_check_sum

    def __str__(self):
        return str(self.block)



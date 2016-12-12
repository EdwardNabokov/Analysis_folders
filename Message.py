from Block import Block
from File import File
from Folder import Folder


class Message:

    def __init__(self):
        self.my_ip = ''
        self.other_ip = ''

    def send_log(self, path_to_folder):
        self.my_log = Folder(path_to_folder).get_log_file()
        print('No prob, man')
        return self.my_ip, self.other_ip, self.my_log

    def get_log(self):
        print('Send me your log please')
        return self.my_ip, self.other_ip

    def send_file(self, path_to_file):
        return File(path_to_file).get_file()

    def get_file(self, path_to_file):
        self.path = path_to_file
        return self.my_ip, self.other_ip, self.path

    def send_sums_each_block(self, other_ip, my_ip, path_folder, path_file):
        print('Sent')
        return other_ip, my_ip

    def get_sums_each_block(self, path_to_file):
        return self.my_ip, self.other_ip, path_to_file



command = 'EXCHANGE_LOG'

if 'EXCHANGE_LOG' == command:
    a = Message()
    b = Message()
    info = a.get_log()
    got_log = b.send_log('C:\\Users\\Edward\\Desktop\\Lab_19_ed')
    if got_log:
        print('Exchanged')
        print(got_log)

commands = ['__GET_LOG__', '__SEND_LOG__', '__GET_FILE__', '__SEND_FILE__', '__GET_BLOCK__', '__SEND_BLOCK__']


class Message:

    def __init__(self):
        self.my_ip = ''
        self.other_ip = ''
        self.path_folder = ''

    def get_log(self):
        print('Send me your log please')
        command = commands[0]
        return command

    def send_log(self, my_log):
        print('No prob, man')
        command = commands[1]
        return command, my_log

    def get_file(self, rel_path_file):
        print('Hey... Could you send me file?  -> ', rel_path_file)
        command = commands[2]
        return command, rel_path_file

    def send_file(self, file):
        print('Sure... Here it is')
        command = commands[3]
        return command, file

    def get_block(self, block_obj):
        print('Pss... i need block - > ', block_obj )
        command = commands[4]
        return command, block_obj

    def send_block(self, block):
        print('Here it is, your block')
        command = commands[5]
        return command, block


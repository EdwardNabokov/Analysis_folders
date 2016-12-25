import pickle


class Message:

    def __init__(self, command, meta, data):
        self.command = pickle.dumps(command)
        self.meta = pickle.dumps(meta)
        if type(data) == str:
            self.data = b''
        else:
            self.data = data

    def command_size(self):
        return len(self.command)

    def meta_size(self):
        return len(self.meta)

    def data_size(self):
        return len(self.data)

    def decode_command(self):
        return pickle.loads(self.command)

    def decode_meta(self):
        return pickle.loads(self.meta)

    def total_size(self):
        return self.command_size() + self.meta_size() + self.data_size()

    def __str__(self):
        return "{}\t-\t{}".format(self.decode_command(), self.decode_meta())
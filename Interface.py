import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import asyncio
import quamash
import socket
import logging
from ListenServer import ListenServer
from ConnectionHandler import ConnectionHandler



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Synchronisation'
        self.left = 300
        self.top = 200
        self.width = 700
        self.height = 500
        self.path_to_folder = ''
        self.my_ip = ''
        self.my_port = ''
        self.connect_ip = ''
        self.connect_port = ''
        self.green = "QWidget { color:#32CD32;}"
        self.red = "QWidget { color:#FF0000; }"
        self.greenb = "QWidget { background-color:#32CD32;}"
        self.redb = "QWidget { background-color:#FF0000; }"
        self.initUI()

    def initUI(self):
        self.move(self.left, self.top)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Synchronization ")
        self.setWindowIcon(QIcon('sync_icon.jpg'))

        self.set_folder_options()
        self.set_ip()
        self.set_port()
        self.set_connection()
        self.set_listening()
        self.set_logger()
        self.set_my_info(self.my_ip, str(self.my_port))
        self.set_other_info()
        self.set_layout_main()

        self.select_folder.clicked.connect(lambda: self.openFileNamesDialog())
        self.button_connection.clicked.connect(lambda: self.connectTo())
        self.button_listening.clicked.connect(lambda: self.pushed_listen())
        self.show()

    def pushed_listen(self):
        self.select_folder.setDisabled(True)
        self.button_listening.setDisabled(True)
        self.my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        self.my_port = self.get_open_port()
        self.my_ip_label.setText(str(self.my_ip))
        self.my_port_label.setText(str(self.my_port))
        server = ListenServer(loop, self.path_to_folder)
        coro = asyncio.start_server(server.start, self.my_ip, self.my_port, loop=loop)
        asyncio.ensure_future(coro)

    def get_open_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def set_my_info(self, my_ip, my_port):
        self.ip_add_horizontal = QHBoxLayout()
        self.my_ip_label = self.set_label(my_ip, 9, True)
        self.ip_label2 = self.set_label('IP Address', 11, True)
        self.ip_add_horizontal.addWidget(self.ip_label2)
        self.ip_add_horizontal.addWidget(self.my_ip_label)

        self.port_horizontal = QHBoxLayout()
        self.port_label = self.set_label('port', 11, True)
        self.my_port_label = self.set_label(str(my_port), 9, True)
        self.port_horizontal.addWidget(self.port_label)
        self.port_horizontal.addWidget(self.my_port_label)

        self.ip_port_listen_vertical = QVBoxLayout()
        self.ip_port_listen_vertical.addLayout(self.ip_add_horizontal)
        self.ip_port_listen_vertical.addLayout(self.port_horizontal)

    def set_other_info(self):
        self.ip_port_connect_vertical = QVBoxLayout()
        self.ip_port_connect_vertical.addLayout(self.ip_name)
        self.ip_port_connect_vertical.addLayout(self.port_name)

    def connectTo(self):
        if len(self.connect_ip) == 0:
            self.ip_address.setStyleSheet(self.redb)
        else:
            self.ip_address.setDisabled(True)
            if len(self.connect_port) == 0:
                self.port.setStyleSheet(self.redb)
            else:
                self.port.setDisabled(True)
                self.path.setDisabled(True)
                self.select_folder.setDisabled(True)
                self.select_folder.setDisabled(True)
                self.button_listening.setDisabled(True)
                self.button_connection.setDisabled(True)
                coro = loop.create_task(
                    ConnectionHandler.runHandler(loop, (self.connect_ip, self.connect_port), self.path_to_folder))
                asyncio.ensure_future(coro)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=options))
        if folder:
            self.path.setText(folder)
            self.path_to_folder = folder + os.sep
            self.button_listening.setEnabled(True)
            self.button_connection.setEnabled(True)

    def set_listening(self):
        self.button_listening = QPushButton('Listen')
        self.button_listening.setFont(QFont('Serif', 10))
        self.button_listening.setFixedSize(100, 30)
        self.button_listening.setDisabled(True)

    def set_layout_main(self):
        self.layout = QFormLayout(self)
        self.layout.setSpacing(5)
        self.folder_layoutV = QVBoxLayout()
        self.folder_layoutH = QHBoxLayout()
        self.ip_port_grid = QVBoxLayout()

        self.folder_layoutH.addWidget(self.path)
        self.folder_layoutH.addWidget(self.select_folder)
        self.folder_layoutV.addWidget(self.folder_to_sync)
        self.folder_layoutV.addLayout(self.folder_layoutH)
        self.folder_layoutV.setSpacing(5)

        self.ip_port_grid.addLayout(self.ip_name)
        self.ip_port_grid.addLayout(self.port_name)

        self.my_info = QGroupBox('My information')
        self.my_info.setFixedSize(400, 90)
        self.my_info.setLayout(self.ip_port_listen_vertical)

        self.listen_info = QHBoxLayout()
        self.listen_info.addWidget(self.button_listening)
        self.listen_info.addWidget(self.my_info)

        self.another_info = QGroupBox('Client information')
        self.another_info.setFixedSize(400, 90)
        self.another_info.setLayout(self.ip_port_connect_vertical)

        self.connect_info = QHBoxLayout()
        self.connect_info.addWidget(self.button_connection)
        self.connect_info.addWidget(self.another_info)

        self.listen_part = QGroupBox('Listen')
        self.listen_part.setLayout(self.listen_info)

        self.connect_part = QGroupBox('Connect')
        self.connect_part.setLayout(self.connect_info)
        self.listen_connect_partsV = QVBoxLayout()
        self.listen_connect_partsV.addWidget(self.listen_part)
        self.listen_connect_partsV.addWidget(self.connect_part)

        self.layout.addRow(self.folder_layoutV)
        self.layout.addRow(self.listen_connect_partsV)
        self.layout.addRow(self.logger_name)

    def set_connection(self):
        self.button_connection = QPushButton('Connect')
        self.button_connection.setFont(QFont('Serif', 10))
        self.button_connection.setFixedSize(100, 30)
        self.button_connection.setDisabled(True)

    def set_ip(self):
        self.ip_address = QLineEdit()
        self.ip_address.setFixedSize(300, 25)
        ip_add_font = QFont('Serif', 9)
        ip_add_font.setFamily('Times New Roman')
        self.ip_address.setPlaceholderText(' enter ip address...')
        self.ip_address.setFont(ip_add_font)
        self.ip_address.setMaxLength(15)
        self.ip_label = self.set_label('IP Address', 11, True)
        self.ip_address.editingFinished.connect(self.textchangedIP)
        self.ip_name = QHBoxLayout()
        self.ip_name.addWidget(self.ip_label)
        self.ip_name.addWidget(self.ip_address)
        self.ip_name.setSpacing(5)

    def set_label(self, text, how_big, bold):
        ip_l = QLabel()
        ip_l.setText(text)
        ip_font = QFont('Serif', how_big)
        ip_font.setBold(bold)
        ip_l.setFont(ip_font)
        return ip_l

    def textchangedIP(self):
        try:
            host_bytes = self.ip_address.text().split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b <= 255]
            if len(host_bytes) == 4 and len(valid) == 4:
                self.connect_ip = self.ip_address.text()
                self.ip_address.setStyleSheet(self.green)
            else:

                self.ip_address.setStyleSheet(self.red)
        except:
            self.ip_address.setStyleSheet(self.red)

    def set_port(self):
        self.port = QLineEdit()
        self.port.setFixedSize(300, 25)
        port_add_font = QFont('Serif', 10)
        port_add_font.setFamily('Times New Roman')
        self.port.setPlaceholderText(' enter port...')
        self.port.setFont(QFont(port_add_font))
        self.port.setMaxLength(5)
        self.port.editingFinished.connect(self.textchangedPORT)
        self.port_label = QLabel()
        self.port_label.setText('port ')
        port_font = QFont('Serif', 10)
        port_font.setBold(True)
        self.port_label.setFont(port_font)
        self.port_name = QHBoxLayout()
        self.port_name.addWidget(self.port_label)
        self.port_name.addWidget(self.port)
        self.port_name.setSpacing(5)

    def textchangedPORT(self):
        try:
            valid = [int(char) for char in self.port.text()]
            if len(valid) <= 5:
                self.connect_port = self.port.text()
                self.port.setStyleSheet(self.green)
            else:
                self.port.setStyleSheet(self.red)
        except:
            self.port.setStyleSheet(self.red)

    def set_folder_options(self):
        self.folder_to_sync = QLabel('Select folder to sync: ')
        self.path = QTextBrowser()
        self.path.setFixedSize(540, 27)
        self.path.setFont(QFont('Serif', 10))
        self.select_folder = QPushButton('Select Folder')
        self.select_folder.setFont(QFont('Serif', 13))

    def set_logger(self):
        self.output_logger_name = QLabel('Logger output')
        self.output_logger_name.setFont(QFont('Serif', 10))

        logTextBox = QPlainTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter("%(asctime)s\t%(message)s", "%H:%M:%S"))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.INFO)

        self.logger_name = QVBoxLayout()
        self.logger_name.addWidget(self.output_logger_name)
        self.logger_name.addWidget(logTextBox.widget)
        self.logger_name.setSpacing(5)


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        ex = App()
        app.exec_()
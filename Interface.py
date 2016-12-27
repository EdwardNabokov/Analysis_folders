import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import asyncio
import quamash
from ListenServer import ListenServer
from ConnectionHandler import ConnectionHandler



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Synchronisation'
        self.left = 300
        self.top = 200
        self.width = 700
        self.height = 400
        self.path_to_folder = ''
        self.my_ip = ''
        self.my_port = ''
        self.connect_ip = ''
        self.connect_port = ''
        self.green = "QWidget { color:#32CD32;}"
        self.red = "QWidget { color:#FF0000; }"
        self.greenb = "QWidget { background-color:#32CD32;}"
        self.redb = "QWidget { background-color:#FF0000; }"

        a = ListenServer(loop, '/Users/Alexander/Google/')
        coro = asyncio.start_server(a.start, '0.0.0.0', 8888, loop=loop)
        asyncio.ensure_future(coro)

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
        self.set_layout_main()

        self.select_folder.clicked.connect(lambda: self.openFileNamesDialog())
        self.button_connection.clicked.connect(lambda: self.checkEveryThing())
        #self.button_listening.clicked.connect()
        self.show()

    def checkEveryThing(self):
        try:
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
                self.output_logger.setText(self.path_to_folder)

                coro = loop.create_task(
                    ConnectionHandler.runHandler(loop, (self.connect_ip, self.connect_port), self.path_to_folder))
                asyncio.ensure_future(coro)
        except:
            self.output_logger.setText('Smth went wrong')

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=options))
        if folder:
            self.path.setText(folder)
            self.path_to_folder = folder
            self.button_listening.setEnabled(True)
            self.button_connection.setEnabled(True)

    def set_listening(self):
        self.button_listening = QPushButton('Listen')
        self.button_listening.setFont(QFont('Serif', 10))
        self.button_listening.setFixedSize(100, 30)
        self.button_listening.setDisabled(True)

    def set_layout_main(self):
        self.layout = QFormLayout(self)
        self.layout.setSpacing(40)
        self.folder_grid = QHBoxLayout()
        self.ip_port_grid = QHBoxLayout()

        self.folder_grid.addWidget(self.path)
        self.folder_grid.addWidget(self.select_folder)
        self.ip_port_grid.addLayout(self.ip_name)
        self.ip_port_grid.addLayout(self.port_name)
        self.my_info = QGroupBox('My information')
        self.horiz = QHBoxLayout()
        self.horiz.addWidget(self.button_connection)
        self.horiz.addWidget(self.button_listening)
        self.horiz.addWidget(self.my_info)

        self.layout.addRow(self.folder_grid)
        self.layout.addRow(self.ip_port_grid)
        self.layout.addRow(self.horiz)
        self.layout.addRow(self.logger_name)

    def set_connection(self):
        self.button_connection = QPushButton('Connect')
        self.button_connection.setFont(QFont('Serif', 10))
        self.button_connection.setFixedSize(100, 30)
        self.button_connection.setDisabled(True)

    def set_ip(self):
        self.ip_address = QLineEdit()
        self.ip_address.setFixedSize(300, 25)
        ip_add_font = QFont('Serif', 10)
        ip_add_font.setFamily('Times New Roman')
        self.ip_address.setPlaceholderText(' enter ip address...')
        self.ip_address.setFont(ip_add_font)
        self.ip_address.setMaxLength(15)
        self.ip_label = QLabel()
        self.ip_label.setText('IP-Address')
        ip_font = QFont('Serif', 11)
        ip_font.setBold(True)
        self.ip_label.setFont(ip_font)
        self.ip_address.editingFinished.connect(self.textchangedIP)
        self.ip_name = QVBoxLayout()
        self.ip_name.addWidget(self.ip_label)
        self.ip_name.addWidget(self.ip_address)
        self.ip_name.setSpacing(5)

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
        self.port.setObjectName("port")
        self.port.setPlaceholderText(' enter port...')
        self.port.setFont(QFont(port_add_font))
        self.port.setMaxLength(5)
        self.port.editingFinished.connect(self.textchangedPORT)
        self.port_label = QLabel()
        self.port_label.setText('Port ')
        port_font = QFont('Serif', 11)
        port_font.setBold(True)
        self.port_label.setFont(port_font)
        self.port_name = QVBoxLayout()
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
        self.path = QTextBrowser()
        self.path.setFixedSize(540, 27)
        self.path.setFont(QFont('Serif', 10))
        self.select_folder = QPushButton('Select Folder')
        self.select_folder.setFont(QFont('Serif', 13))

    def set_logger(self):
        self.output_logger = QTextBrowser()
        self.output_logger_name = QLabel('Logger output')
        self.output_logger_name.setFont(QFont('Serif', 10))

        self.logger_name = QVBoxLayout()
        self.logger_name.addWidget(self.output_logger_name)
        self.logger_name.addWidget(self.output_logger)
        self.logger_name.setSpacing(5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        ex = App()
        app.exec_()
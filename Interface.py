import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Synchronisation'
        self.left = 300
        self.top = 200
        self.width = 700
        self.height = 400
        self.initUI()
        self.path_to_folder = ''
        self.my_ip = ''
        self.my_port = ''
        self.another_comp_IP_address = ''
        self.another_comp_port = ''
        self.green = "QWidget { color:#32CD32;}"
        self.red = "QWidget { color:#FF0000; }"
        self.greenb = "QWidget { background-color:#32CD32;}"
        self.redb = "QWidget { background-color:#FF0000; }"

    def initUI(self):
        self.move(self.left, self.top)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Synchronization ")
        self.setWindowIcon(QIcon('sync_icon.jpg'))

        self.set_folder_options()
        self.set_ip()
        self.set_port()
        self.set_button_sync()
        self.set_logger()
        self.set_layout_main()

        self.select_folder.clicked.connect(lambda: self.openFileNamesDialog())
        self.sync.clicked.connect(lambda: self.checkEveryThing())
        self.show()

    def checkEveryThing(self):
        try:
            if len(self.another_comp_IP_address) == 0:
                self.ip_address.setStyleSheet(self.redb)
            else:
                self.ip_address.setDisabled(True)

            if len(self.another_comp_port) == 0:
                self.port.setStyleSheet(self.redb)
            else:
                self.port.setDisabled(True)
                self.path.setDisabled(True)
                self.select_folder.setDisabled(True)
                self.output_logger.setText(self.path_to_folder)
                # self.start_()
        except:
            self.output_logger.setText('Smth went wrong')

    # def start_(self):
    #     start_listening()
    #     start_connection(self.another_comp_IP_address, self.another_comp_port, self.path_to_folder)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=options))
        if folder:
            self.path.setText(folder)
            self.path_to_folder = folder
            self.sync.setEnabled(True)

    def progressbar(self):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()

    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

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
        self.horiz.addWidget(self.sync)
        self.horiz.addWidget(self.my_info)


        self.layout.addRow(self.folder_grid)
        self.layout.addRow(self.ip_port_grid)
        self.layout.addRow(self.horiz)
        self.layout.addRow(self.logger_name)

    def set_button_sync(self):
        self.sync = QPushButton('Sync')
        self.sync.setFont(QFont('Serif', 10))
        self.sync.setFixedSize(100, 30)
        self.sync.setDisabled(True)

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
                self.another_comp_IP_address = self.ip_address.text()
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
                self.another_comp_port = self.port.text()
                self.port.setStyleSheet(self.green)
            else:
                self.port.setStyleSheet(self.red)
        except:
            self.port.setStyleSheet(self.red)

    def set_folder_options(self):
        self.path = QTextBrowser()
        self.path.setFixedSize(570, 27)
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
    ex = App()
    app.exec_()
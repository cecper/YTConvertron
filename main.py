from appeke import convert
import sys
from PySide2.QtWidgets import QApplication,QDialog,QLineEdit,QLabel,QComboBox,QPushButton,QVBoxLayout,QTextEdit,QFileDialog
from PySide2.QtGui import QScreen,Qt,QIcon
import threading

from PySide2.QtCore import Signal


class Form(QDialog):

    started = Signal()
    finished = Signal()
    def __init__(self, parent=None):
        
            super(Form, self).__init__(parent)
            self.setWindowFlags(self.windowFlags()^ Qt.WindowContextHelpButtonHint)
            self.setGeometry(0, 0, 800, 600)
            center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            geo = self.frameGeometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

            self.file="."
            self.setWindowTitle("YTConverter")

            self.url = QLineEdit()
            labelUrl = QLabel("video url:",self)
            labelUrl.setAlignment(Qt.AlignHCenter |Qt.AlignBottom)
            labelUrl.setBuddy(self.url)
            
            self.cb = QComboBox()
        
            self.cb.addItem('MP3')
            self.cb.addItem('playlistMp3')
            self.cb.addItem('playlistMp4')
            self.cb.addItem('LowMP4')
            self.cb.addItem('720MP4')
            self.cb.addItem('1080fps24MP4')
            self.cb.addItem('1080fps60MP4')
            
            self.button = QPushButton("Convert")
            self.fileDialogButton = QPushButton("Select video ouput location")
            self.exitButton = QPushButton("Exit")
            self.commandLineOut = QTextEdit(readOnly=True)

            self.url.setFixedWidth(600)
            self.button.setFixedWidth(600)
            self.cb.setFixedWidth(600)
            self.fileDialogButton.setFixedWidth(600)
            self.exitButton.setFixedWidth(600)
            self.commandLineOut.setFixedWidth(600)

            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)  
            layout.addWidget(self.url)
            layout.addWidget(self.cb)
            layout.addWidget(self.fileDialogButton)
            layout.addWidget(self.button)
            layout.addWidget(self.exitButton)
            layout.addWidget(self.commandLineOut)


            self.setLayout(layout)

            self.button.clicked.connect(self.clickMethod)
            self.fileDialogButton.clicked.connect(self.fileSelect)
            self.exitButton.clicked.connect(self.shutdownClick)


    def clickMethod(self):
            try:
                threading.Thread(target=self.convertInClass(), daemon=True).start()
                self.commandLineOut.append(f'Your video was found and downloaded in {self.file}.')
            except:
                self.commandLineOut.append('Your video was not found, check the url. If you\'re trying to download a playlist select the right dropdown item.')

    def convertInClass(self):
        self.cbString=str(self.cb.currentText())
        self.urlString=self.url.text()
        print(self.urlString)
        print(self.cbString)
        
        self.started.emit()
        
        convert(self.urlString,self.cbString,self.file)
        self.finished.emit()

    def fileSelect(self):
        self.file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(self.file)     
        self.commandLineOut.append(f"You have selected: {self.file} as output file location.")
        
    def shutdownClick(self):
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('index.png'))
    form = Form()
    form.show()
    sys.exit(app.exec_())


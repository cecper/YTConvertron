from youtube_converter import convert
import sys
from PySide2.QtWidgets import QWidget,QTabWidget,QApplication,QDialog,QLineEdit,QComboBox,QPushButton,QVBoxLayout,QTextEdit,QFileDialog
from PySide2.QtGui import QScreen,Qt,QIcon
import threading

from PySide2.QtCore import Signal


class Form(QDialog):

    started = Signal()
    finished = Signal()

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.file="."
        self.setWindowFlags(self.windowFlags()^ Qt.WindowContextHelpButtonHint)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("YTConverter")
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)

        #Centreer window
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        # Initialize tab screen
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        
        # Add tabs
        tabs.addTab(tab1,"Youtube Converter")
        tabs.addTab(tab2,"File Format Converter")

        self.url_input_field = QLineEdit()
        self.url_input_field.setPlaceholderText("Enter URL here")
        
        button = QPushButton("Convert")
        fileDialogButton = QPushButton("Select video ouput location")
        exitButton = QPushButton("Exit")
        self.commandLineOut = QTextEdit(readOnly=True)
        self.commandLineOut.setPlaceholderText("Output")
        
        cb_array = ['MP3','playlistMp3','playlistMp4','LowMP4','720MP4','1080fps24MP4','1080fps60MP4']
        self.cb = QComboBox()
        self.cb.addItems(cb_array)
        
        # Create first tab
        tab1.layout = QVBoxLayout(self)
        tab1.layout.addWidget(self.url_input_field)
        tab1.layout.addWidget(self.cb)
        tab1.layout.addWidget(fileDialogButton)
        tab1.layout.addWidget(button)
        tab1.layout.addWidget(exitButton)
        tab1.layout.addWidget(self.commandLineOut)
        tab1.setLayout(tab1.layout)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  
        
        layout.addWidget(tabs)
        
        self.setLayout(layout)

        button.clicked.connect(self.click_method)
        fileDialogButton.clicked.connect(self.file_select)
        exitButton.clicked.connect(self.shutdown_click)

    def click_method(self):
        try:
            threading.Thread(target=self.convert_in_class(), daemon=True).start()
            self.commandLineOut.append(f'Your video was found and downloaded in {self.file}.')
        except Exception as e:
            self.commandLineOut.append(str(e))

    def convert_in_class(self):
        cbString=str(self.cb.currentText())
        urlString=self.url_input_field.text()
        print(urlString)
        print(cbString)
        
        self.started.emit()
        convert(urlString,cbString,self.file)
        self.finished.emit()

    def file_select(self):
        self.file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(self.file)
        self.commandLineOut.append(f"You have selected: {self.file} as output file location.")

    def commandLineOut_append(self, text):
        self.commandLineOut.append(text)

    def shutdown_click(self):
        sys.exit(app.exec_())
        


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('yt_icon.png'))
    form = Form()
    form.show()
    sys.exit(app.exec_())
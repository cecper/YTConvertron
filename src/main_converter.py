from youtube_converter import convert
import sys
from PySide6.QtWidgets import QWidget,QTabWidget,QApplication,QDialog,QLineEdit,QComboBox,QPushButton,QVBoxLayout,QTextEdit,QFileDialog
from PySide6.QtGui import QScreen,Qt,QIcon
#from PySide2.QtCore import QRunnable, Slot, QThreadPool #multithreading WIP 

import configparser


class Form(QDialog):

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
        
        # tab1
        tab1.layout = QVBoxLayout(self)
        tab1.layout.addWidget(self.url_input_field)
        tab1.layout.addWidget(self.cb)
        tab1.layout.addWidget(fileDialogButton)
        tab1.layout.addWidget(button)
        tab1.layout.addWidget(exitButton)
        tab1.layout.addWidget(self.commandLineOut)
        tab1.setLayout(tab1.layout)

        # tab2
        tab2.layout = QVBoxLayout(self)
        tab2.setLayout(tab2.layout)

        #set layout for application
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  
        layout.addWidget(tabs)
        self.setLayout(layout)

        #set button functions
        button.clicked.connect(self.click_method)
        fileDialogButton.clicked.connect(self.file_select)
        exitButton.clicked.connect(self.shutdown_click)

    def file_select(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(file)

        config = configparser.ConfigParser()
        config.read('user_pref.ini')

        # when section does not exist, add section otherwise update default_path value
        try:
            config.add_section('file_saving_pref')
        except configparser.DuplicateSectionError:
            pass
        config['file_saving_pref']['default_path'] = file    # update
        #create file if it does not yet exist
        with open('user_pref.ini', 'w') as configfile:    # save
            config.write(configfile)

        self.commandLineOut.append(f"You have selected: {self.file} as output file location.")

    def convert_in_class(self):
        cbString=str(self.cb.currentText())
        urlString=self.url_input_field.text()
        print(urlString)
        print(cbString)

        
    # read values from a section
        try:
            config = configparser.ConfigParser()
            config.read('user_pref.ini')
            string_val = config.get('file_saving_pref', 'default_path')
            print(string_val)
        except configparser.NoSectionError:
            config.add_section('file_saving_pref')
            config['file_saving_pref']['default_path'] = "."    # update
            with open('user_pref.ini', 'w') as configfile:    # save
                config.write(configfile)

        convert(urlString,cbString,config.get('file_saving_pref', 'default_path'))

    def click_method(self):
        try:
            self.convert_in_class()
            self.commandLineOut.append(f'Your video was found and downloaded in {self.file}.')
        except Exception as e:
            self.commandLineOut.append(str(e))

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
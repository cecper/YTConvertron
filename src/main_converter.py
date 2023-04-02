from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import configparser
from PyInstaller.utils.hooks import collect_data_files

class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)
        self.file="."
        self.setWindowFlags(self.windowFlags()^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setGeometry(0, 0, 1000, 800)
        self.setWindowTitle("YTConverter")
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon('yt_icon.png'))
        self.process = QtCore.QProcess(self)
        
        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.onUpdateText)

        #Centreer window
        center = QtGui.QScreen.availableGeometry(QtGui.QGuiApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        # Initialize tab screen
        tabs = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tabs.addTab(tab1,"Youtube Converter")
        tabs.addTab(tab2,"File Format Converter")

        #create input fields tab1
        self.url_input_field = QtWidgets.QLineEdit()
        self.url_input_field.setPlaceholderText("Enter URL here")
        self.button = QtWidgets.QPushButton("Convert")
        fileDialogButton = QtWidgets.QPushButton("Select video ouput location")
        stopProcess = QtWidgets.QPushButton("Stop Converting")
        exitButton = QtWidgets.QPushButton("Exit")
        self.commandLineOut = QtWidgets.QTextEdit(readOnly=True)
        self.commandLineOut.setPlaceholderText("Output")
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(['MP3','lowest quality MP4','medium quality MP4','highest quality MP4','highest framerate/quality MP4'])
        
        # tab1
        tab1.layout = QtWidgets.QVBoxLayout(self)
        tab1.layout.addWidget(self.url_input_field)
        tab1.layout.addWidget(self.cb)
        tab1.layout.addWidget(fileDialogButton)
        tab1.layout.addWidget(self.button)
        tab1.layout.addWidget(stopProcess)
        stopProcess.setEnabled(False)
        tab1.layout.addWidget(exitButton)
        tab1.layout.addWidget(self.commandLineOut)
        tab1.setLayout(tab1.layout)

        #create input fields tab2
        filepath_to_mp3 = QtWidgets.QPushButton("Select MP3 to convert")
        self.cb_mp3_convert = QtWidgets.QComboBox()
        self.cb_mp3_convert.addItems(['WAV','MP4','M4A','FLAC','WMA','AAC'])

        # tab2
        tab2.layout = QtWidgets.QVBoxLayout(self)
        tab2.layout.addWidget(filepath_to_mp3)
        tab2.layout.addWidget(self.cb_mp3_convert)
        tab2.setLayout(tab2.layout)

        #set layout for application
        layout = QtWidgets.QVBoxLayout()
        #layout.setAlignment(QtGui.AlignCenter)  
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.show()

        #set button functions tab1
        self.button.clicked.connect(self.click_method)
        stopProcess.clicked.connect(self.stop)
        fileDialogButton.clicked.connect(self.file_select)
        exitButton.clicked.connect(self.shutdown_click)

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.onUpdateText)

         #Disable buttons when process (convert()) is running
        self.process.started.connect(lambda: self.button.setEnabled(False))
        self.process.started.connect(lambda: fileDialogButton.setEnabled(False))
        self.process.started.connect(lambda: stopProcess.setEnabled(True))

        #Enable buttons when process (convert()) is finished
        self.process.finished.connect(lambda: self.button.setEnabled(True))
        self.process.finished.connect(lambda: fileDialogButton.setEnabled(True)) 
        self.process.finished.connect(lambda: stopProcess.setEnabled(False)) 

    def file_select(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

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
        
    # read values from a section
        try:
            config = configparser.ConfigParser()
            config.read('user_pref.ini')
            string_val = config.get('file_saving_pref', 'default_path')

        except configparser.NoSectionError:
            config.add_section('file_saving_pref')
            config['file_saving_pref']['default_path'] = "."    # update
            with open('user_pref.ini', 'w') as configfile:    # save
                config.write(configfile)

        string_val = config.get('file_saving_pref', 'default_path')

        self.process.start('python.exe',['youtube_converter.py', f'{urlString}', f'{cbString}',f'{string_val}'])
        
        # Disable the conversion button while the process is running
        self.button.setEnabled(False)
        # Check the status of the process periodically
        self.onUpdateText()

    def click_method(self):
        try:
            self.convert_in_class()
            #self.commandLineOut.append(f'Your video was found and downloaded in {self.file}.')
        except Exception as e:
            self.commandLineOut.append(str(e))

    def commandLineOut_append(self, text):
        self.commandLineOut.append(text)

    def onUpdateText(self):
        display_string=(str(self.process.readLine()))
        display_string=display_string.replace(r"b'","")
        display_string=display_string.replace(r"b'\r'","")
        display_string=display_string.replace(r"b'\n'","")
        display_string=display_string.replace(r"\r","")
        self.commandLineOut.append(display_string) 

    def stop(self):
        self.process.kill()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def shutdown_click(self):
        sys.exit(app.exec_())
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
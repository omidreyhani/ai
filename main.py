from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import voice  # This would be your AI application
import record
import threading

class AIApp(QMainWindow):
    def __init__(self):
      super().__init__()
      self.setWindowTitle('My AI Application')
      self.initUI()
      self.recoding = False
      self.cancelRecordingEvent = threading.Event()
      self.width = 800
      self.height = 600
      self.recordinThread = None
     
    def initUI(self):
      

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Layout and widgets
        layout = QVBoxLayout()
        layout.spacing = 20
        layout.spacing = 200



        self.recordButton = QPushButton('Record and run AI Model')
        self.recordButton.clicked.connect(self.onRecordClicked)
        layout.addWidget(self.recordButton)

        self.resultLabel = QLabel('Results will be shown here')
        layout.addWidget(self.resultLabel)

        self.centralWidget.setLayout(layout)

    def onRecordClicked(self):
        if self.recoding:
            # We're currently recording, so stop the recording
            self.cancelRecordingEvent.set()  # Signal to cancel the recording
            self.recordButton.setText('Record Voice')
            self.recordinThread.join()
            print('Stopped recording...')
            self.resultLabel.setText(voice.load("output.wav"))
        else:
            # We're not currently recording, so start the recording
           self.recordinThread = threading.Thread(target=record.record, args=(self.cancelRecordingEvent,))
           self.recordinThread.start()
           self.recordButton.setText('Stop Recording')
           self.cancelRecordingEvent.clear()
           print('Recording...')

        self.recoding = not self.recoding 


if __name__ == '__main__':
    app = QApplication([])
    window = AIApp()
    window.show()
    app.exec_()

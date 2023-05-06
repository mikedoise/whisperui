from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QToolBar, QComboBox, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtGui import QAction, Qt
import whisper

class TranscriptionPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a text control to display the transcription
        self.transcription_text = QTextEdit(self)

        # Create buttons to save the transcription and play/pause the audio
        self.play_pause_button = QPushButton("Play", self)

        # Add the controls to a layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.transcription_text)
        layout.addWidget(self.play_pause_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

class TranscriptionFrame(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        menu_bar = QMenuBar(self)
        file_menu = QMenu("File", menu_bar)
        open_item = file_menu.addAction("Open Audio File")
        save_item = file_menu.addAction("Save Transcription")
        exit_item = file_menu.addAction("Exit")
        menu_bar.addMenu(file_menu)

        model_menu = QMenu("Model", menu_bar)
        base_item = model_menu.addAction("Base")
        small_item = model_menu.addAction("Small")
        large_item = model_menu.addAction("Large")
        menu_bar.addMenu(model_menu)

        self.setMenuBar(menu_bar)

        open_item.triggered.connect(self.on_open)
        save_item.triggered.connect(self.on_save)
        exit_item.triggered.connect(self.close)

        base_item.triggered.connect(lambda: self.transcription_model.setCurrentText("base"))
        small_item.triggered.connect(lambda: self.transcription_model.setCurrentText("small"))
        large_item.triggered.connect(lambda: self.transcription_model.setCurrentText("large"))

        # Create the toolbar
        self.toolbar = QToolBar(self)
        self.transcription_model = QComboBox(self.toolbar)
        self.transcription_model.addItems(["base", "small", "large"])
        self.toolbar.addWidget(self.transcription_model)
        self.open_tool = QAction("Open", self.toolbar)
        self.save_tool = QAction("Save", self.toolbar)
        self.toolbar.addAction(self.open_tool)
        self.toolbar.addAction(self.save_tool)
        self.addToolBar(self.toolbar)

        self.open_tool.triggered.connect(self.on_open)
        self.save_tool.triggered.connect(self.on_save)

        # Create the TranscriptionPanel
        self.panel = TranscriptionPanel(self)

        # Bind the play/pause button's click event to a handler function
        self.panel.play_pause_button.clicked.connect(self.on_play_pause)

        # Set up the frame
        self.setWindowTitle("Transcription")
        self.setCentralWidget(self.panel)
        self.resize(800, 600)
        self.show()

    def on_play_pause(self):
        # Update the button label and start or pause the audio
        if self.panel.play_pause_button.text() == "Play":
            self.panel.play_pause_button.setText("Pause")
            # TODO: Start playing the audio
        else:
            self.panel.play_pause_button.setText("Play")
            # TODO: Pause the audio

    def on_save(self):
        file_dialog = QFileDialog(self, "Save transcription", "", "Text files (*.txt);;All files (*)")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "w") as file:
                file.write(self.panel.transcription_text.toPlainText())

    def on_open(self):
        file_dialog = QFileDialog(self, "Open file for transcription", "", "Audio files (*.mp3 *.wav .m4a);;All files ()")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            model = whisper.load_model(self.transcription_model.currentText())
            result = model.transcribe(file_path)
            transcription = result["text"]
            self.panel.transcription_text.setPlainText(transcription)

if __name__ == '__main__':
    app = QApplication()
    frame = TranscriptionFrame()
    app.exec()
import wx
import whisper

class TranscriptionPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a choice control to select the model
        self.transcription_model = wx.Choice(self, choices=["base", "small", "large"])
        
        # Create a text control to display the transcription
        self.transcription_text = wx.TextCtrl(self, value="", style=wx.TE_MULTILINE)

        # Create buttons to save the transcription and play/pause the audio
        self.save_button = wx.Button(self, label="Save Transcription")
        self.open_button = wx.Button(self, label="Open File")
        self.play_pause_button = wx.Button(self, label="Play")

        # Add the controls to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.transcription_model, 0, wx.CENTER)
        sizer.Add(self.transcription_text, 1, wx.EXPAND)
        sizer.Add(self.save_button, 0, wx.ALIGN_CENTER)
        sizer.Add(self.play_pause_button, 0, wx.ALIGN_CENTER)
        sizer.Add(self.open_button, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)

class TranscriptionFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_item = file_menu.Append(wx.ID_OPEN, "Open Audio File")
        save_item = file_menu.Append(wx.ID_SAVE, "Save Transcription")
        file_menu.Append(wx.ID_EXIT, "Exit")
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)

         # Create the toolbar
        self.toolbar = self.CreateToolBar()
        self.choice = wx.Choice(self.toolbar, choices=["base", "small", "large"])
        self.choice.SetSize((120, -1))
        self.toolbar.AddControl(self.choice)
        open_tool = self.toolbar.AddTool(wx.ID_OPEN, "Open", wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN))
        save_tool = self.toolbar.AddTool(wx.ID_SAVE, "Save", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE))
        self.toolbar.Realize()

        
        # Create the TranscriptionPanel
        self.panel = TranscriptionPanel(self)

        # Bind the play/pause button's click event to a handler function
        self.panel.play_pause_button.Bind(wx.EVT_BUTTON, self.on_play_pause)

        # Bind the save button's click event to a handler function
        self.panel.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.panel.open_button.Bind(wx.EVT_BUTTON, self.on_open)

        # Set up the frame
        self.SetTitle("Transcription")
        self.SetSize(800, 600)
        self.Centre()
        self.Show()

    def on_play_pause(self, event):
        # Update the button label and start or pause the audio
        if self.panel.play_pause_button.GetLabel() == "Play":
            self.panel.play_pause_button.SetLabel("Pause")
            # TODO: Start playing the audio
        else:
            self.panel.play_pause_button.SetLabel("Play")
            # TODO: Pause the audio

    def on_save(self, event):
        # Show a save dialog to choose the file location
        with wx.FileDialog(self, "Save transcription", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # user cancelled the dialog

            # Save the transcription to the chosen file
            with open(file_dialog.GetPath(), "w") as file:
                file.write(self.panel.transcription_text.GetValue())

    def on_open(self, event):
        # Show an open file dialog to choose the file to transcribe
        with wx.FileDialog(self, "Open file for transcription", wildcard="Audio files (*.mp3;*.wav;*.m4a)|*.mp3;*.wav;*.m4a",
                           style=wx.FD_OPEN) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # user cancelled the dialog

            # Transcribe the chosen file
            filepath = file_dialog.GetPath()
            model = whisper.load_model(self.panel.transcription_model.GetStringSelection())
            result = model.transcribe(filepath)
            transcription = result["text"]
            self.panel.transcription_text.SetValue(transcription)

if __name__ == '__main__':
    app = wx.App()
    frame = TranscriptionFrame(None)
    app.MainLoop()
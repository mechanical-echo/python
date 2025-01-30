from kivy.uix.screenmanager import ScreenManager
from components.settings_window import SettingsWindow

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'settings_window' not in self.screen_names:
            self.add_widget(SettingsWindow(name='settings_window'))

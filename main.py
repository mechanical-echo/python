from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from components.login_window import LoginWindow
from components.window_manager import WindowManager
from components.note_creation_window import NoteCreationWindow
from components.note_item_view import NoteItemView
from components.notes_view import NotesView
from components.note_edit_window import NoteEditWindow
from components.user_view import UserView
from kivy.utils import platform
from kivy.core.window import Window
from kivy.config import Config
from kivy.animation import Animation

class LoginApp(App):
    def build(self):
        if platform not in ('android', 'ios'):
            Window.size = (1000, 600)

        if platform in ('android', 'ios'):
            Window.fullscreen = 'auto'

        wm = WindowManager()
        return wm


if __name__ == '__main__':
    print("test")
    LoginApp().run()

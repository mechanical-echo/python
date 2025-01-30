from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.graphics import Color

class SettingsWindow(Screen):
    background_colors = ListProperty(['Balts', 'Pelēks', 'Zils', 'Zaļš', 'Oranža'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.dropdown = DropDown()
        for color in self.background_colors:
            btn = Button(text=color, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.set_background_color(btn.text))
            self.dropdown.add_widget(btn)

        self.add_widget(layout)

    def set_background_color(self, color):
        notes_view = self.manager.get_screen('notes_view')

        if color == 'Balts':
            notes_view.background_color = [1, 1, 1, 1]
        elif color == 'Pelēks':
            notes_view.background_color = [0.83, 0.83, 0.83, 1]
        elif color == 'Zils':
            notes_view.background_color = [0.68, 0.85, 0.9, 1]
        elif color == 'Zaļš':
            notes_view.background_color = [0.56, 0.93, 0.56, 1]
        elif color == 'Oranža':
            notes_view.background_color = [1, 0.49, 0.31, 1]

        self.dropdown.dismiss()

    def go_back(self):
        self.manager.current = 'notes_view'


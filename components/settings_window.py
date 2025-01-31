from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.metrics import dp

class SettingsWindow(Screen):
    preview_color = ListProperty([1, 1, 1, 1])
    current_color = StringProperty("Balts")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_color_dropdown()
        
    def create_color_dropdown(self):
        self.dropdown = DropDown()
        colors = [
            ("Balts", [1, 1, 1, 1]),
            ("Pelēks", [0.83, 0.83, 0.83, 1]),
            ("Zils", [0.68, 0.85, 0.9, 1]),
            ("Zaļš", [0.56, 0.93, 0.56, 1]),
            ("Oranžs", [1, 0.49, 0.31, 1])
        ]
        
        for color_name, color_value in colors:
            btn = Button(
                text=color_name,
                size_hint_y=None,
                height=dp(44),
                background_color=color_value
            )
            btn.bind(on_release=lambda btn: self.select_color(btn.text, btn.background_color))
            self.dropdown.add_widget(btn)

    def select_color(self, color_name, color_value):
        self.current_color = color_name
        self.preview_color = color_value
        notes_view = self.manager.get_screen('notes_view')
        notes_view.background_color = color_value
        self.dropdown.dismiss()

    def back_to_main(self):
        self.manager.current = 'notes_view'


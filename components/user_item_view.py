from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import csv
import os

class UserItemView(BoxLayout):
    username = StringProperty("")
    name = StringProperty("")
    surname = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, .75)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)

        user_info = BoxLayout(orientation='vertical', size_hint_x=0.6)
        user_info.add_widget(Label(text=f"Username: {self.username}", font_size=dp(16), bold=True, halign='left'))
        user_info.add_widget(Label(text=f"Name: {self.name} {self.surname}", font_size=dp(14), halign='left'))
        self.add_widget(user_info)

        button_container = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=dp(10))
        
        edit_button = Button(text="Edit", size_hint_x=0.5, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        edit_button.bind(on_press=self.edit_user)
        button_container.add_widget(edit_button)

        delete_button = Button(text="Delete", size_hint_x=0.5, background_color=(1, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        delete_button.bind(on_press=self.delete_user)
        button_container.add_widget(delete_button)

        self.add_widget(button_container)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def edit_user(self, instance):
        print(f"Editing user: {self.username}")

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        name_input = TextInput(text=self.name, hint_text="Name", multiline=False)
        surname_input = TextInput(text=self.surname, hint_text="Surname", multiline=False)
        save_button = Button(text="Save", size_hint_y=None, height=50)

        content.add_widget(name_input)
        content.add_widget(surname_input)
        content.add_widget(save_button)

        popup = Popup(title=f"Edit {self.username}", content=content, size_hint=(0.8, 0.4))
        popup.open()

        def save_changes(instance):
            new_name = name_input.text
            new_surname = surname_input.text

            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            users_csv_path = os.path.join(project_root, 'csv', 'users.csv')

            rows = []
            with open(users_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['username'] == self.username:
                        row['name'] = new_name
                        row['surname'] = new_surname
                    rows.append(row)

            with open(users_csv_path, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['username', 'password', 'name', 'surname', 'role']
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)

            popup.dismiss()

            if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'load_users'):
                self.parent.parent.load_users()

        save_button.bind(on_press=save_changes)

    def delete_user(self):
        print(f"Deleting user: {self.username}")
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')

        rows = []
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] != self.username:
                    rows.append(row)

        with open(users_csv_path, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['username', 'password', 'name', 'surname', 'role']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)

        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'load_users'):
            self.parent.parent.load_users()
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import csv

class UserEditWindow(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    name_input = ObjectProperty(None)
    surname_input = ObjectProperty(None)
    current_user = StringProperty("")

    def load_user_data(self, username):
        self.current_user = username
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] == username:
                    self.username_input.text = row['username']
                    self.password_input.text = row['password']
                    self.name_input.text = row['name']
                    self.surname_input.text = row['surname']
                    break

    def save_user_data(self):
        old_username = self.current_user
        new_username = self.username_input.text
        password = self.password_input.text
        name = self.name_input.text
        surname = self.surname_input.text
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        notes_csv_path = os.path.join(project_root, 'csv', 'notes.csv')
        
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] == new_username and row['username'] != old_username:
                    self.show_popup("Error", "Username already exists. Please choose a different username.")
                    return
        updated_rows = []        
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] == old_username:
                    row['username'] = new_username
                    row['password'] = password
                    row['name'] = name
                    row['surname'] = surname
                updated_rows.append(row)

        with open(users_csv_path, 'w', newline='', encoding='utf-8') as file:        
            fieldnames = ['username', 'password', 'name', 'surname', 'role']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(updated_rows)

        updated_notes = []
        with open(notes_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['user_id'] == old_username:
                    row['user_id'] = new_username
                updated_notes.append(row)

        with open(notes_csv_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['user_id', 'note_id', 'filename', 'category', 'color', 'created_at']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(updated_notes)

        self.show_popup("Success", "Profile updated successfully!")

    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message), 
            size_hint=(None, None), 
            size=(400, 200)
        )
        popup.open()

    def back_to_main(self):
        self.manager.current = 'notes_view'

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
import os
import csv

class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    status_message = StringProperty('')

    def verify_user(self, username, password):
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            csv_path = os.path.join(project_root, 'csv', 'users.csv')
            
            if os.path.exists(csv_path):
                with open(csv_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter='\t')
                    for row in reader:
                        if row['username'] == username and row['password'] == password:
                            return True
                return False
            
            self.status_message = "CSV fails nav atrasts"
            return False
            
        except Exception as e:
            self.status_message = f"CSV faila lasīšanas kļūda: {e}"
            return False

    def login_button(self):
        if self.verify_user(self.username.text, self.password.text):
            self.manager.current = 'notes_view'
            notes_screen = self.manager.get_screen('notes_view')
            notes_screen.current_user = self.username.text
            notes_screen.check_admin_role(self.username.text)
            notes_screen.load_user_notes(self.username.text)
            self.username.text = ""
            self.password.text = ""
        else:
            self.status_message = "Neveiksmīga autorizācija!"

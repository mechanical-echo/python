from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.metrics import dp
import csv
import os

class UserListItem(BoxLayout):
    username = StringProperty('')
    name = StringProperty('')
    surname = StringProperty('')
    role = StringProperty('')

    def edit_user(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        name_input = TextInput(text=self.name, hint_text='Vārds', multiline=False)
        surname_input = TextInput(text=self.surname, hint_text='Uzvārds', multiline=False)
        role_input = TextInput(text=self.role, hint_text='Loma', multiline=False)
        
        save_btn = Button(text='Saglabāt', size_hint_y=None, height=dp(40))
        
        content.add_widget(Label(text='Rediģēt lietotāju'))
        content.add_widget(name_input)
        content.add_widget(surname_input)
        content.add_widget(role_input)
        content.add_widget(save_btn)
        
        popup = Popup(title='Rediģēt lietotāju',
                     content=content,
                     size_hint=(None, None),
                     size=(400, 300))
        
        def save(instance):
            self.update_user_data(name_input.text, surname_input.text, role_input.text)
            popup.dismiss()
            
        save_btn.bind(on_press=save)
        popup.open()

    def update_user_data(self, new_name, new_surname, new_role):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        
        rows = []
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] == self.username:
                    row['name'] = new_name
                    row['surname'] = new_surname
                    row['role'] = new_role
                rows.append(row)
        
        with open(users_csv_path, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['lietotājvārds', 'parole', 'vārds', 'uzvārds', 'loma']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)
            
        self.name = new_name
        self.surname = new_surname
        self.role = new_role

    def delete_user(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=f'Vai tiešām vēlaties dzēst lietotāju {self.username}?'))
        
        buttons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        cancel_btn = Button(text='Atcelt')
        confirm_btn = Button(text='Apstiprināt')
        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)
        content.add_widget(buttons)
        
        popup = Popup(title='Apstiprināt dzēšanu',
                     content=content,
                     size_hint=(None, None),
                     size=(400, 200))
        
        def confirm(instance):
            self.confirm_delete()
            popup.dismiss()
            
        def cancel(instance):
            popup.dismiss()
            
        confirm_btn.bind(on_press=confirm)
        cancel_btn.bind(on_press=cancel)
        popup.open()

    def confirm_delete(self):
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
            
        self.parent.remove_widget(self)

class UserView(Screen):
    def on_enter(self):
        self.load_users()

    def load_users(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        
        users_container = self.ids.users_container
        users_container.clear_widgets()
        
        if os.path.exists(users_csv_path):
            with open(users_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    user_item = UserListItem(
                        username=row['username'],
                        name=row['name'],
                        surname=row['surname'],
                        role=row['role']
                    )
                    users_container.add_widget(user_item)

    def add_new_user(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        username_input = TextInput(hint_text='Username', multiline=False)
        password_input = TextInput(hint_text='Password', multiline=False, password=True)
        name_input = TextInput(hint_text='Name', multiline=False)
        surname_input = TextInput(hint_text='Surname', multiline=False)
        role_input = TextInput(hint_text='Role', multiline=False)
        
        save_btn = Button(text='Add User', size_hint_y=None, height=dp(40))
        
        content.add_widget(username_input)
        content.add_widget(password_input)
        content.add_widget(name_input)
        content.add_widget(surname_input)
        content.add_widget(role_input)
        content.add_widget(save_btn)
        
        popup = Popup(title='Add New User',
                     content=content,
                     size_hint=(None, None),
                     size=(400, 400))
        
        def save(instance):
            self.save_new_user(
                username_input.text,
                password_input.text,
                name_input.text,
                surname_input.text,
                role_input.text
            )
            popup.dismiss()
            self.load_users()
            
        save_btn.bind(on_press=save)
        popup.open()

    def save_new_user(self, username, password, name, surname, role):
        if not all([username, password, name, surname, role]):
            return
            
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        
        new_user = {
            'username': username,
            'password': password,
            'name': name,
            'surname': surname,
            'role': role
        }
        
        rows = []
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            rows = list(reader)
            
        rows.append(new_user)
        
        with open(users_csv_path, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['username', 'password', 'name', 'surname', 'role']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)

    def back_to_main(self):
        self.manager.current = 'notes_view'
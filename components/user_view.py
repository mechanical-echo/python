from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from components.user_item_view import UserItemView
import csv
import os

class UserView(Screen):
    users_data = []

    def __init__(self, **kwargs):
        super(UserView, self).__init__(**kwargs)
        self.orientation = 'vertical'

    def on_kv_post(self, *args):
        super(UserView, self).on_kv_post(*args)
        self.load_users()

    def load_users(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')

        self.users_data = []
        if os.path.exists(users_csv_path):
            with open(users_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    self.users_data.append({
                        'username': row['username'],
                        'name': row['name'],
                        'surname': row['surname']
                    })

        self.update_users_view()
    def back_to_main(self):
        self.manager.current = 'notes_view'
        
    def update_users_view(self):
        if hasattr(self, 'ids') and 'users_container' in self.ids:
            users_container = self.ids.users_container
            users_container.clear_widgets()

            if self.users_data:
                for user in self.users_data:
                    user_item = UserItemView(username=user['username'], name=user['name'], surname=user['surname'])
                    users_container.add_widget(user_item)
            else:
                no_users_label = Label(text="No users found", size_hint_y=None, height=100)
                users_container.add_widget(no_users_label)
        else:
            print("users_container not found in self.ids")
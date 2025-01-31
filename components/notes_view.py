from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty, ColorProperty, BooleanProperty
import os
import csv
from kivy.uix.label import Label
from components.note_item_view import NoteItemView
from components.user_edit_window import UserEditWindow
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class NotesView(Screen):
    notes_data = ListProperty([])
    colors_data = ListProperty([])
    current_user = StringProperty("")
    background_color = ColorProperty([1, 0.93, 0.93, 1])
    is_admin = BooleanProperty(False)
    
    sort_order_date = True
    sort_order_title = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes_label = Label(text="", size_hint_y=None, height=100)
        self.add_widget(self.notes_label)

    def open_user_management(self):
        self.manager.current = 'user_view'

    def edit_profile(self):
        self.manager.current = 'user_edit'
        edit_screen = self.manager.get_screen('user_edit')
        edit_screen.load_user_data(self.current_user)

    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Sveicināti!"
        self.manager.current = 'login'

    def create_note(self):
        self.manager.get_screen('note_creation').current_user = self.current_user
        self.manager.current = 'note_creation'

    def load_user_notes(self, username):
        self.notes_data = []
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        notes_csv_path = os.path.join(project_root, 'csv', 'notes.csv')
        colors_csv_path = os.path.join(project_root, 'csv', 'colors.csv')
        
        if os.path.exists(notes_csv_path):
            with open(notes_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['user_id'] == username:
                        self.notes_data.append({
                            'color':        row['color'],
                            'note_id':      row['note_id'],
                            'category':     row['category'],
                            'filename':     row['filename'],
                            'created_at':   row['created_at']
                        })

        self.colors_data = []

        if os.path.exists(colors_csv_path):
            with open(colors_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    self.colors_data.append({
                        'color_id': row['color_id'],
                        'r':        row['r'],
                        'g':        row['g'],
                        'b':        row['b'],
                    })

        self.notes_data.sort(key=lambda x: x['created_at'], reverse=True)
        self.update_notes_view()

    def update_notes_view(self):
        notes_container = self.ids.notes_container
        notes_container.clear_widgets()
        
        if self.notes_data:
            for note in self.notes_data:
                color_id_from_note_data = note['color']
            
                for colors_data_row in self.colors_data:
                    if colors_data_row['color_id'] == color_id_from_note_data:
                        color = colors_data_row

                note_item = NoteItemView(
                    filename        = note['filename'], 
                    created_at      = note['created_at'],
                    note_title      = note['note_id'],
                    note_category   = note['category'],
                    color_red       = color['r'],
                    color_green     = color['g'],
                    color_blue      = color['b'],
                    current_user    = self.current_user
                )
                note_item.current_user = self.current_user
                notes_container.add_widget(note_item)
        else:
            no_notes_label = Label(text="No notes found", size_hint_y=None, height=100)
            notes_container.add_widget(no_notes_label)

    def edit_note(self, filename):
        self.manager.current = 'note_edit'
        edit_screen = self.manager.get_screen('note_edit')
        edit_screen.load_note_data(filename)

    def open_settings(self):
        self.manager.current = 'settings_window'

    def sort_notes_by_date(self):
        self.sort_order_date = not self.sort_order_date
        self.notes_data.sort(key=lambda x: x['created_at'], reverse=not self.sort_order_date)
        self.update_notes_view()

    def sort_notes_by_title(self):
        self.sort_order_title = not self.sort_order_title
        self.notes_data.sort(key=lambda x: x['note_id'], reverse=not self.sort_order_title)
        self.update_notes_view()

    def check_admin_role(self, username):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        users_csv_path = os.path.join(project_root, 'csv', 'users.csv')
        
        with open(users_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['username'] == username:
                    self.is_admin = row['role'] == 'admin'
                    break

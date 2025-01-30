from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
import os
import csv
from kivy.uix.label import Label
from components.note_item_view import NoteItemView

class NotesView(Screen):
    notes_data = ListProperty([])
    colors_data = ListProperty([])
    current_user = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes_label = Label(text="", size_hint_y=None, height=100)
        self.add_widget(self.notes_label)

    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Welcome!"
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

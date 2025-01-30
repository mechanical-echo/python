from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.button import Button
from kivy.app import App  # Importing App
import os
import csv

class NoteItemView(BoxLayout):
    note_text = StringProperty('')
    note_title = StringProperty('')
    note_category = StringProperty('')
    created_at = StringProperty('')
    filename = StringProperty('')
    selected = BooleanProperty(False)
    color_red = NumericProperty(0)
    color_green = NumericProperty(0)
    color_blue = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None

        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            note_path = os.path.join(project_root, 'notes', self.filename)
            with open(note_path, 'r', encoding='utf-8') as file:
                self.note_text = file.read()
        except Exception as e:
            self.note_text = f"Error reading note: {e}"


    def edit_note(self):
        # Correctly access the screen manager
        app = App.get_running_app()
        app.root.current = 'note_edit'  # Switch to the new edit screen
        edit_screen = app.root.get_screen('note_edit')
        edit_screen.load_note_data(self.filename, self.note_text, self.note_title, self.note_category)

    def delete_note(self):
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            note_path = os.path.join(project_root, 'notes', self.filename)
            os.remove(note_path)

            notes_csv_path = os.path.join(project_root, 'csv', 'notes.csv')
            updated_rows = []
            with open(notes_csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                for row in reader:
                    if row['filename'] != self.filename:
                        updated_rows.append(row)

            with open(notes_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['user_id', 'note_id', 'filename', 'category', 'color', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(updated_rows)

            self.parent.remove_widget(self)

        except Exception as e:
            self.note_text = f"Error deleting note: {e}"

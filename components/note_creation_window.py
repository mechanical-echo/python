from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
import os
import csv
import uuid
from datetime import datetime

class NoteCreationWindow(Screen):
    note_text = ObjectProperty(None)
    note_title_text = ObjectProperty(None)
    current_user = StringProperty("")
    chosen_color = StringProperty("melns")
    chosen_category = StringProperty("darbs")

    def create_color_dropdown(self, button):
        dropdown = DropDown()
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        colors_csv_path = os.path.join(project_root, 'csv', 'colors.csv')
        
        with open(colors_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                btn = Button(
                    text=row['color_id'],
                    size_hint_y=None,
                    height=44,
                    background_color=(float(row['r']), float(row['g']), float(row['b']), 1)
                )
                btn.bind(on_release=lambda btn: self.select_color(btn.text, dropdown))
                dropdown.add_widget(btn)
        
        dropdown.open(button)
    
    def select_color(self, color_id, dropdown):
        self.chosen_color = color_id
        dropdown.dismiss()

    def create_category_dropdown(self, button):
        dropdown = DropDown()
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        categories_csv_path = os.path.join(project_root, 'csv', 'categories.csv')
        
        with open(categories_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                btn = Button(
                    text=row['name'],
                    size_hint_y=None,
                    height=44,
                )
                btn.bind(on_release=lambda btn: self.select_category(btn.text, dropdown))
                dropdown.add_widget(btn)
        
        dropdown.open(button)
    
    def select_category(self, category_id, dropdown):
        self.chosen_category = category_id
        dropdown.dismiss()

    def save_note(self):
        if not self.note_text.text.strip():
            self.show_popup("Kļūda", "Piezīmes teksts nedrīkst būt tukšs!")
            return

        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            notes_dir = os.path.join(project_root, 'notes')
            csv_dir = os.path.join(project_root, 'csv')
            os.makedirs(notes_dir, exist_ok=True)

            note_id = str(uuid.uuid4())
            filename = f"{note_id}.txt"
            note_path = os.path.join(notes_dir, filename)
            with open(note_path, 'w', encoding='utf-8') as note_file:
                note_file.write(self.note_text.text)

            notes_csv_path = os.path.join(csv_dir, 'notes.csv')
            file_exists = os.path.exists(notes_csv_path)
            
            with open(notes_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='\t')
                if not file_exists:
                    csvwriter.writerow(['user_id', 'note_id', 'filename', 'category', 'color', 'created_at'])
                
                csvwriter.writerow([
                    self.current_user,
                    self.note_title_text.text,
                    filename,
                    self.chosen_category,
                    self.chosen_color,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
            
            self.show_popup("Veiksmīgi", "Piezīme saglabāta!")
            self.note_text.text = ""
            self.note_title_text.text = ""
            self.back_to_main()
            notes_screen = self.manager.get_screen('notes_view')
            notes_screen.load_user_notes(self.current_user)
            notes_screen.current_user = (self.current_user)
            self.manager.current = 'notes_view'
            
        except Exception as e:
            self.show_popup("Kļūda", f"Neizdevās saglabāt piezīmi: {str(e)}")

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
        self.note_text.text = ""
        self.note_title_text.text = ""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import platform
from kivy.config import Config
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import csv
import os
import sys
import uuid
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, BooleanProperty


if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'mouse_cursor_enable', 1)
Config.write()

class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    status_message = StringProperty('')
    status_color = (0.4, 0.2, 0.6, 1)

    def verify_user(self, username, password):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, 'users.csv')
            
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
            main_screen = self.manager.get_screen('main')
            main_screen.current_user = self.username.text
            main_screen.update_welcome_text()
            
            self.status_message = "Veiksmīga autorizācija!"
            self.status_color = (0.2, 0.8, 0.2, 1)
            self.username.text = ""
            self.password.text = ""

            self.manager.current = 'main'
        else:
            self.status_message = "Neveiksmīga autorizācija!"
            self.status_color = (0.8, 0.2, 0.2, 1)

class MainWindow(Screen):
    current_user = StringProperty("")
    welcome_text = StringProperty("Sveiks!")

    def update_welcome_text(self):
        self.welcome_text = f"Sveiks, {self.current_user}!"

    def view_notes(self):
        notes_screen = self.manager.get_screen('notes_view')
        notes_screen.load_user_notes(self.current_user)
        self.manager.current = 'notes_view'

    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message), 
            size_hint=(None, None), 
            size=(400, 200)
        )
        popup.open()

    def create_note(self):
        self.manager.current = 'note_creation'

    def edit_note(self):
        # Logic to edit a note
        pass

    def logout_button(self):
        self.current_user = ""
        self.welcome_text = "Welcome!"
        self.manager.current = 'login'

    def on_enter(self):
        self.manager.get_screen('note_creation').current_user = self.current_user


class WindowManager(ScreenManager):
    pass

class LoginApp(App):
    def build(self):
        if platform not in ('android', 'ios'):
            Window.size = (600, 400)

        if platform in ('android', 'ios'):
            Window.fullscreen = 'auto'

        return WindowManager()
    
    def animate_button(self, button):
        colors = [
            (0.5, 0.3, 0.7),  # Purple
            (0.7, 0.3, 0.5),  # Pink
            (0.7, 0.3, 0.5),  # Pink
            (0.5, 0.3, 0.7)   # Purple
        ]
        
        anim = None
        duration = 2
        
        for i, color in enumerate(colors[:-1]):
            next_color = colors[i + 1]
            
            new_anim = Animation(
                r=next_color[0],
                g=next_color[1],
                b=next_color[2],
                duration=duration,
                transition='out_sine'
            )
            
            if anim is None:
                anim = new_anim
            else:
                anim += new_anim
        
        anim.repeat = True
        anim.start(button)


class NoteCreationWindow(Screen):
    note_text = ObjectProperty(None)
    current_user = StringProperty("")

    def save_note(self):
        if not self.note_text.text.strip():
            self.show_popup("Kļūda", "Piezīmes teksts nedrīkst būt tukšs!")
            return

        try:
            # Generate unique filename
            note_id = str(uuid.uuid4())
            filename = f"{note_id}.txt"
            
            # Create notes directory if it doesn't exist
            notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notes')
            os.makedirs(notes_dir, exist_ok=True)
            
            # Save note text file
            note_path = os.path.join(notes_dir, filename)
            with open(note_path, 'w', encoding='utf-8') as note_file:
                note_file.write(self.note_text.text)
            
            # Update notes CSV
            notes_csv_path = os.path.join(notes_dir, 'notes.csv')
            file_exists = os.path.exists(notes_csv_path)
            
            with open(notes_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter='\t')
                if not file_exists:
                    csvwriter.writerow(['user_id', 'note_id', 'filename', 'created_at'])
                
                csvwriter.writerow([
                    self.current_user, 
                    note_id, 
                    filename, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
            
            self.show_popup("Veiksmīgi", "Piezīme saglabāta!")
            self.note_text.text = ""
            
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
        self.manager.current = 'main'
        self.note_text.text = ""

class NoteItemView(BoxLayout):
    note_text = StringProperty('')
    created_at = StringProperty('')
    filename = StringProperty('')
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None  # Prevent shrinking
        self.height = 100  # Set a fixed height or adjust based on content

        print(f"NoteItemView __init__ called, filename: {self.filename}")

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            note_path = os.path.join(current_dir, 'notes', self.filename)
            print(f"Note path: {note_path}")
            with open(note_path, 'r', encoding='utf-8') as file:
                self.note_text = file.read()
                print(f"Note text: {self.note_text}")
        except Exception as e:
            self.note_text = f"Error reading note: {e}"
            print(f"Error reading note: {e}")

class NotesView(Screen):
    notes_data = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes_label = Label(text="", size_hint_y=None, height=100)
        self.add_widget(self.notes_label)

    def load_user_notes(self, username):
        self.notes_data = []
        notes_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notes', 'notes.csv')

        if os.path.exists(notes_csv_path):
            with open(notes_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    if row['user_id'] == username:
                        self.notes_data.append({
                            'filename': row['filename'],
                            'created_at': row['created_at']
                        })

        self.notes_data.sort(key=lambda x: x['created_at'], reverse=True)
        self.update_notes_view()

    def update_notes_view(self):
        notes_container = self.ids.notes_container
        notes_container.clear_widgets()
        
        print(f"Notes data: {self.notes_data}")
        if self.notes_data:
            for note in self.notes_data:
                note_item = NoteItemView(filename=note['filename'], created_at=note['created_at'])
                notes_container.add_widget(note_item)
        else:
            no_notes_label = Label(text="No notes found", size_hint_y=None, height=100)
            notes_container.add_widget(no_notes_label)

    def back_to_main(self):
        self.manager.current = 'main'


if __name__ == '__main__':
    LoginApp().run()

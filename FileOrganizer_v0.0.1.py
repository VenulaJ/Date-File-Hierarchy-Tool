import kivy
import os
import platform
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

kivy.require('2.3.1')

class FileOrganizer(BoxLayout):
    def __init__(self, **kwargs):
        
        super().__init__(
            orientation='vertical', 
            size=(600, 200), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, 
            **kwargs)
        
        beginning_button_and_text_box = BoxLayout(
            orientation='horizontal', 
            spacing=10,
            size_hint_y=None)
        
        destination_button_and_text_box = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None)
        
        input_directory_text_box = TextInput(
            text='displays input directory after choosing', 
            multiline=False, 
            readonly=True)
        
        output_directory_text_box = TextInput(
            text='displays output directory after choosing', 
            multiline=False, 
            readonly=True)
       
        beginning_button_and_text_box.add_widget(input_directory_text_box)
        destination_button_and_text_box.add_widget(output_directory_text_box)
    
        browse_beginning_directory_button = Button(
            text='Browse Beginning Directory', 
            on_release=self.open_file_explorer, 
            size_hint_y=None)
        
        browse_destination_directory_button = Button(
            text='Browse Destination Directory', 
            on_release=self.open_file_explorer, 
            size_hint_y=None)
        
        beginning_button_and_text_box.add_widget(browse_beginning_directory_button)
        destination_button_and_text_box.add_widget(browse_destination_directory_button)
        
        self.add_widget(beginning_button_and_text_box)
        self.add_widget(destination_button_and_text_box)
        
    def open_file_explorer(self, instance):
        if platform.system() == 'Windows':
            subprocess.Popen(['explorer.exe'], shell=True)
          
class FileOrganizerApp(App):
    def build(self):
        self.icon = 'FileOrganizer_icon.png' 
        return FileOrganizer()

if __name__=="__main__":
    FileOrganizerApp().run()

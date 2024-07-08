from kivy.app import App
from kivy.uix.button import Button
import os
import sys

class MileageTrackerApp(App):
    def build(self):
        print(f"Python version: {sys.version}")
        print(f"Kivy version: {App.version}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir('.')}")
        return Button(text='Hello World')

if __name__ == '__main__':
    MileageTrackerApp().run()

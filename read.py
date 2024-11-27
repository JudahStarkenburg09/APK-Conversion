from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

class VerseScreen(FloatLayout):
    verse_text = StringProperty("")  # To hold and dynamically update verse text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.verses = []  # List to hold split verses

        # Responsive Label for displaying verse text
        self.label = Label(
            text=self.verse_text,
            font_size='20sp',
            size_hint=(0.9, 0.5),  # Adjust width and height
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle',
            text_size=(self.width * 0.9, None)  # Wrap text within the label width
        )
        self.label.bind(size=self._update_text_size)
        self.add_widget(self.label)

        # Button for the right side (Next Verse)
        self.right_area = Button(
            background_color=(0, 0, 0, 0),  # Transparent background
            size_hint=(0.5, 1),  # Right half of the screen
            pos_hint={'x': 0.5, 'y': 0},
            on_press=self.next_verse
        )
        self.add_widget(self.right_area)

        # Button for the left side (Previous Verse)
        self.left_area = Button(
            background_color=(0, 0, 0, 0),  # Transparent background
            size_hint=(0.5, 1),  # Left half of the screen
            pos_hint={'x': 0, 'y': 0},
            on_press=self.previous_verse
        )
        self.add_widget(self.left_area)

        # Label for "Next >" text
        self.next_label = Label(
            text="Next >",
            font_size='16sp',
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.8, 'y': 0.9},
            halign='right',
            valign='middle',
            color=(1, 1, 1, 1)  # Black text
        )
        self.add_widget(self.next_label)

        # Label for "< Previous" text
        self.previous_label = Label(
            text="< Previous",
            font_size='16sp',
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0, 'y': 0.9},
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)  # Black text
        )
        self.add_widget(self.previous_label)

    def _update_text_size(self, *args):
        self.label.text_size = (self.label.width * 0.9, None)

    def load_text(self, text):
        # Split the verse into smaller strings by period
        self.verses = [v.strip() for v in text.split('.') if v.strip()]
        self.current_index = 0
        self.update_label()

    def update_label(self):
        if 0 <= self.current_index < len(self.verses):
            self.verse_text = self.verses[self.current_index]
            self.label.text = self.verse_text
        else:
            self.verse_text = "End of verse" if self.current_index >= len(self.verses) else ""
            self.label.text = self.verse_text

    def next_verse(self, instance):
        if self.current_index < len(self.verses) - 1:
            self.current_index += 1
            self.update_label()

    def previous_verse(self, instance):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_label()


class BibleApp(App):
    def build(self):
        screen_manager = ScreenManager()
        verse_screen = VerseScreen()
        screen = Screen(name="memorize")
        screen.add_widget(verse_screen)
        screen_manager.add_widget(screen)

        # Load a sample verse
        sample_text = ("In the beginning, God created the heavens and the earth. "
                       "Now the earth was formless and empty. "
                       "Darkness was over the surface of the deep, and the Spirit of God "
                       "was hovering over the waters.")
        verse_screen.load_text(sample_text)

        return screen_manager


if __name__ == '__main__':
    BibleApp().run()

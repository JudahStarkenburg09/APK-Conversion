from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse

class ComplexApp(App):
    def build(self):
        # Set up the main layout
        self.layout = FloatLayout()

        # Label to show the value of the slider
        self.label = Label(text="Slider Value: 0", size_hint=(None, None), size=(200, 50), pos=(10, 400))
        self.layout.add_widget(self.label)

        # Slider to change the value
        self.slider = Slider(min=0, max=100, value=0, size_hint=(None, None), size=(400, 50), pos=(10, 300))
        self.slider.bind(value=self.update_label)
        self.layout.add_widget(self.slider)

        # Text input to enter custom text
        self.text_input = TextInput(hint_text="Enter text", size_hint=(None, None), size=(400, 50), pos=(10, 200))
        self.layout.add_widget(self.text_input)

        # Button that changes text based on the input
        self.button = Button(text="Update Text", size_hint=(None, None), size=(200, 50), pos=(10, 100))
        self.button.bind(on_press=self.update_text)
        self.layout.add_widget(self.button)

        # Draw a circle on the canvas
        with self.layout.canvas.before:
            Color(1, 0, 0)  # Red color
            self.circle = Ellipse(pos=(250, 100), size=(50, 50))  # Initial position and size of the circle

        return self.layout

    def update_label(self, instance, value):
        # Update the label text with the slider value
        self.label.text = f"Slider Value: {int(value)}"
        # Move the circle based on the slider value (the X position)
        self.circle.pos = (250 + value, 100)

    def update_text(self, instance):
        # Change the label text to the entered text
        self.label.text = f"Custom Text: {self.text_input.text}"

if __name__ == '__main__':
    ComplexApp().run()

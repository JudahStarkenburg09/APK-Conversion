from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

# Define WIDTH and HEIGHT dynamically based on the window size
WIDTH = Window.width
HEIGHT = Window.height

# Position values based on the screen width
x1_16 = Window.width / 16
x1_12 = Window.width / 12
x1_10 = Window.width / 10
x1_8 = Window.width / 8
x1_6 = Window.width / 6
x1_4 = Window.width / 4
x1_2 = Window.width / 2  # 50% of the width

y1_16 = Window.height / 16
y1_12 = Window.height / 12
y1_10 = Window.height / 10
y1_8 = Window.height / 8
y1_6 = Window.height / 6
y1_4 = Window.height / 4
y1_2 = Window.height / 2  # 50% of the height

# Define text sizes based on window height
smlText1 = Window.height / 40
smlText2 = Window.height / 35
medText1 = Window.height / 30
medText2 = Window.height / 25
lrgText = Window.height / 20
exLrgText = Window.height / 15

class MyApp(App):
    def build(self):
        layout = FloatLayout()

        # Create labels with different text sizes and set x to x1_2
        label1 = Label(
            text="Small Text 1", size_hint=(None, None),
            font_size=smlText1,
            pos=(x1_2, HEIGHT * 0.8)
        )
        label2 = Label(
            text="Small Text 2", size_hint=(None, None),
            font_size=smlText2,
            pos=(x1_2, HEIGHT * 0.7)
        )
        label3 = Label(
            text="Medium Text 1", size_hint=(None, None),
            font_size=medText1,
            pos=(x1_2, HEIGHT * 0.6)
        )
        label4 = Label(
            text="Medium Text 2", size_hint=(None, None),
            font_size=medText2,
            pos=(x1_2, HEIGHT * 0.5)
        )
        label5 = Label(
            text="Large Text", size_hint=(None, None),
            font_size=lrgText,
            pos=(x1_2, HEIGHT * 0.4)
        )
        label6 = Label(
            text="Extra Large Text", size_hint=(None, None),
            font_size=exLrgText,
            pos=(x1_2, HEIGHT * 0.3),
        )

        # Add labels to the layout
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(label3)
        layout.add_widget(label4)
        layout.add_widget(label5)
        layout.add_widget(label6)

        return layout

if __name__ == '__main__':
    MyApp().run()

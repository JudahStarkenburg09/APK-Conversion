from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image  # Import the Image widget
# Run Code

WIDTH = Window.width
HEIGHT = Window.height

# Define WIDTH and HEIGHT dynamically based on the window size

# Position values based on the screen width
x1_16 = WIDTH / 16
x1_12 = WIDTH / 12
x1_10 = WIDTH / 10
x1_8 = WIDTH / 8
x1_6 = WIDTH / 6
x1_4 = WIDTH / 4
x1_2 = WIDTH / 2  # 50% of the width

y1_16 = HEIGHT / 16
y1_12 = HEIGHT / 12
y1_10 = HEIGHT / 10
y1_8 = HEIGHT / 8
y1_6 = HEIGHT / 6
y1_4 = HEIGHT / 4
y1_2 = HEIGHT / 2  # 50% of the height

# Define text sizes based on window height
smlText1 = HEIGHT / 40
smlText2 = HEIGHT / 35
medText1 = HEIGHT / 30
medText2 = HEIGHT / 25
lrgText = HEIGHT / 20
exLrgText = HEIGHT / 15


class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Set color (dark gray in this case)
            Color(0.1, 0.1, 0.1, 1)  # RGBA (0.1, 0.1, 0.1, 1) is dark gray
            # Draw rectangle (x, y, width, height)
            self.rect = Rectangle(pos=(0, 0), size=(WIDTH, y1_8))

class MyApp(App):
    def build(self):
        layout = FloatLayout()

        # Add the main widget (rectangle)
        layout.add_widget(MyWidget())

        # Create an image for the home icon and other icons
        self.home_icon = Image(source='homeIco-s.png', size_hint=(None, None), size=(50, 50), pos=(x1_2, y1_16 / 3))
        self.start_icon = Image(source='homeIco-d.png', size_hint=(None, None), size=(50, 50), pos=(x1_2-x1_4, y1_16 / 3))
        self.search_icon = Image(source='homeIco-d.png', size_hint=(None, None), size=(50, 50), pos=(x1_2+x1_4, y1_16 / 3))

        # Add images to the layout
        layout.add_widget(self.home_icon)
        layout.add_widget(self.start_icon)
        layout.add_widget(self.search_icon)

        # Add text labels for content (initially "home")
        self.page_label = Label(text="Home", font_size=20, size_hint=(None, None), size=(WIDTH, HEIGHT), pos=(0, 0))
        layout.add_widget(self.page_label)

        # Add tap listeners to each image
        self.home_icon.bind(on_touch_down=self.select_home)
        self.start_icon.bind(on_touch_down=self.select_start)
        self.search_icon.bind(on_touch_down=self.select_search)

        return layout

    def select_home(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            self.update_selected_icon(self.home_icon, "Home")

    def select_start(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            self.update_selected_icon(self.start_icon, "Start")

    def select_search(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            self.update_selected_icon(self.search_icon, "Search")

    def update_selected_icon(self, selected_icon, page_name):
        # Update all icons to unselected (default state)
        self.home_icon.source = 'homeIco-d.png'
        self.start_icon.source = 'homeIco-d.png'
        self.search_icon.source = 'homeIco-d.png'

        # Set the selected icon to the selected state
        selected_icon.source = selected_icon.source.replace('d.png', 's.png')

        # Update the page content label with the respective page name
        self.page_label.text = page_name


if __name__ == '__main__':
    MyApp().run()

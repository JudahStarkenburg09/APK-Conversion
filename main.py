from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image  # Import the Image widget

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Set color (dark gray in this case)
            Color(0.1, 0.1, 0.1, 1)  # RGBA (0.1, 0.1, 0.1, 1) is dark gray
            # Draw a rectangle with a size hint that fills the bottom 1/8 of the screen
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = (Window.width, Window.height / 8)
        self.rect.pos = (0, 0)

class MyApp(App):
    def build(self):
        layout = FloatLayout()

        # Add the main widget (rectangle)
        layout.add_widget(MyWidget())

        # Create icons with size and position hints
        self.home_icon = Image(
            source='homeIco-s.png',
            size_hint=(0.1, 0.1),  # 10% of the window width and height
            pos_hint={'center_x': 0.5, 'y': 0.01}  # Center horizontally, 1% from the bottom
        )
        self.start_icon = Image(
            source='startIco-d.png',
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.25, 'y': 0.01}  # Left of center
        )
        self.search_icon = Image(
            source='searchIco-d.png',
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.75, 'y': 0.01}  # Right of center
        )

        # Add images to the layout
        layout.add_widget(self.home_icon)
        layout.add_widget(self.start_icon)
        layout.add_widget(self.search_icon)

        # Add a label with size and position hints to fill most of the screen
        self.page_label = Label(
            text="Home",
            font_size='20sp',
            size_hint=(0.8, 0.8),  # 80% of screen width and height
            pos_hint={'center_x': 0.5, 'center_y': 0.6}  # Centered with a higher Y position
        )
        layout.add_widget(self.page_label)

        # Add tap listeners to each icon image
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
        self.start_icon.source = 'startIco-d.png'
        self.search_icon.source = 'searchIco-d.png'

        # Set the selected icon to the selected state
        selected_icon.source = selected_icon.source.replace('d.png', 's.png')

        # Update the page content label with the respective page name
        self.page_label.text = page_name

if __name__ == '__main__':
    MyApp().run()

# Deselect: #585454
# Select: #a8a4a4

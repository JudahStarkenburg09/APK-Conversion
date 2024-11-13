from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

# Set window size
WIDTH = 367
HEIGHT = 600
Window.size = (WIDTH, HEIGHT)

# Define screen classes for each page
class Page1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Add label to page 1
        label = Label(
            text="Page 1", size_hint=(None, None),
            font_size=HEIGHT / 20,
            pos=(WIDTH / 2 - 50, HEIGHT / 2 - 20)
        )
        layout.add_widget(label)
        self.add_widget(layout)

class Page2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Add label to page 2
        label = Label(
            text="Page 2", size_hint=(None, None),
            font_size=HEIGHT / 20,
            pos=(WIDTH / 2 - 50, HEIGHT / 2 - 20)
        )
        layout.add_widget(label)
        self.add_widget(layout)

class Page3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Add label to page 3
        label = Label(
            text="Page 3", size_hint=(None, None),
            font_size=HEIGHT / 20,
            pos=(WIDTH / 2 - 50, HEIGHT / 2 - 20)
        )
        layout.add_widget(label)
        self.add_widget(layout)

# Define the main app class
class MyApp(App):
    def build(self):
        # Main layout that holds sidebar and screen manager
        main_layout = BoxLayout(orientation='horizontal')

        # Sidebar layout
        sidebar = BoxLayout(orientation='vertical', size_hint=(None, 1), width=80)
        sidebar.add_widget(Button(text="Page 1", on_press=self.change_page))
        sidebar.add_widget(Button(text="Page 2", on_press=self.change_page))
        sidebar.add_widget(Button(text="Page 3", on_press=self.change_page))

        # Screen manager to hold pages
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Page1(name="page1"))
        self.screen_manager.add_widget(Page2(name="page2"))
        self.screen_manager.add_widget(Page3(name="page3"))

        # Add sidebar and screen manager to the main layout
        main_layout.add_widget(sidebar)
        main_layout.add_widget(self.screen_manager)

        return main_layout

    # Change screen page function
    def change_page(self, instance):
        if instance.text == "Page 1":
            self.screen_manager.current = "page1"
        elif instance.text == "Page 2":
            self.screen_manager.current = "page2"
        elif instance.text == "Page 3":
            self.screen_manager.current = "page3"

if __name__ == '__main__':
    MyApp().run()

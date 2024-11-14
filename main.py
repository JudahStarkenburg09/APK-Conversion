from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.1, 0.1, 0.1, 1)  # Dark gray background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        

    def update_rect(self, *args):
        self.rect.size = (Window.width, Window.height / 9)
        self.rect.pos = (0, 0)
    

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scripture="Search to choose your piece of scripture"

    def build(self):
        self.layout = FloatLayout()
        self.current_page_content = []
        self.rect = None  # Add a variable to track the rectangle

        # Add the main widget (rectangle)
        self.layout.add_widget(MyWidget())

        # Create icons
        self.home_icon = Image(source='homeIco-s.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.5, 'y': 0.01})
        self.start_icon = Image(source='startIco-d.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.25, 'y': 0.01})
        self.search_icon = Image(source='searchIco-d.png', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.75, 'y': 0.01})

        # Add icons to layout
        self.layout.add_widget(self.home_icon)
        self.layout.add_widget(self.start_icon)
        self.layout.add_widget(self.search_icon)

        # Add event listeners for icons
        self.home_icon.bind(on_touch_down=lambda instance, touch: self.select_home(instance, touch, _pass=False))
        self.start_icon.bind(on_touch_down=lambda instance, touch: self.select_start(instance, touch, _pass=False))
        self.search_icon.bind(on_touch_down=lambda instance, touch: self.select_search(instance, touch, _pass=False))

        # Initial label for content display
        self.page_label = Label(text="Home", font_size='20sp', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.layout.add_widget(self.page_label)
        self.current_page_content.append(self.page_label)

        return self.layout

    def clear_page_content(self):
        for widget in self.current_page_content:
            self.layout.remove_widget(widget)
        self.current_page_content = []

        # Remove the rectangle if it exists
        if self.rect:
            self.layout.canvas.before.remove(self.rect)
            self.rect = None

    def select_home(self, instance, touch, _pass):
        if instance.collide_point(touch.x, touch.y) or _pass:
            self.clear_page_content()
            self.update_selected_icon(self.home_icon, "Home")
            self.page_label = Label(text="Home", font_size='20sp', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.6})
            self.layout.add_widget(self.page_label)
            self.current_page_content.append(self.page_label)

    def select_start(self, instance, touch, _pass):
        window_width = Window.width
        window_height = Window.height
        if instance.collide_point(touch.x, touch.y) or _pass:
            self.clear_page_content()
            self.update_selected_icon(self.start_icon, "Start")

            self.methodsTitle = Label(
                text="Methods",
                font_size=f'{window_width/16}dp',
                size_hint=(0.8, 0.8),
                pos_hint={'center_x': 0.15, 'center_y': 0.88},
                font_name='impact.ttf'  # Ensure the font file is in the same directory as your script
            )

            self.layout.add_widget(self.methodsTitle)
            self.current_page_content.append(self.methodsTitle)

            # Create and add the button
            read = Button(
                text="Read",
                size_hint=(0.2, 0.075),
                pos_hint={'center_x': 0.15, 'center_y': 0.75},
                background_normal='button1-d.png',  # Set image as background
                background_down='button1-s.png',    # Optional: Set image for the button when pressed
                font_name='impact.ttf',  # Ensure the font file is in the same directory as your script
                font_size=f'{window_width/40}dp',
                border=(0, 0, 0, 0),
                color=(1, 1, 1, 0.8)
            )

            # Create and add the button
            speech = Button(
                text="Speech",
                size_hint=(0.2, 0.075),
                pos_hint={'center_x': 0.15, 'center_y': 0.65},
                background_normal='button1-d.png',  # Set image as background
                background_down='button1-s.png',    # Optional: Set image for the button when pressed
                font_name='impact.ttf',  # Ensure the font file is in the same directory as your script
                font_size=f'{window_width/40}dp',
                border=(0, 0, 0, 0),
                color=(1, 1, 1, 0.8)
            )

            # Create and add the button
            fill_blanks = Button(
                text="Fill Blanks",
                size_hint=(0.2, 0.075),
                pos_hint={'center_x': 0.15, 'center_y': 0.55},
                background_normal='button1-d.png',  # Set image as background
                background_down='button1-s.png',    # Optional: Set image for the button when pressed
                font_name='impact.ttf',  # Ensure the font file is in the same directory as your script
                font_size=f'{window_width/40}dp',
                border=(0, 0, 0, 0),
                color=(1, 1, 1, 0.8)
            )

            audio = Button(
                text="Audio",
                size_hint=(0.2, 0.075),
                pos_hint={'center_x': 0.15, 'center_y': 0.45},
                background_normal='button1-d.png',  # Set image as background
                background_down='button1-s.png',    # Optional: Set image for the button when pressed
                font_name='impact.ttf',  # Ensure the font file is in the same directory as your script
                font_size=f'{window_width/40}dp',
                border=(0, 0, 0, 0),
                color=(1, 1, 1, 0.8)
            )


            # Bind the button to the empty function
            read.bind(on_press=self.empty_function)
            speech.bind(on_press=self.empty_function)
            fill_blanks.bind(on_press=self.empty_function)
            audio.bind(on_press=self.empty_function)

            self.layout.add_widget(read)
            self.layout.add_widget(speech)
            self.layout.add_widget(fill_blanks)
            self.layout.add_widget(audio)

            self.current_page_content.append(read)
            self.current_page_content.append(speech)
            self.current_page_content.append(fill_blanks)
            self.current_page_content.append(audio)

            # Create a rectangle from the top left, width 40% of the screen, height covers entire screen (minus the bottom bar)
            with self.layout.canvas.before:
                Color(0.66, 0.64, 0.64, 0.25)  # Set your desired color (RGB values between 0 and 1)
                self.rect = Rectangle(
                    pos=(0, (Window.height / 9) + (Window.height / 100)),  # bottom-left corner
                    size=(Window.width * 0.3, Window.height)  # 40% of width, full height
                )

            # Get the width and height of the window
            print(f"{window_width} + {window_height}")

            # Calculate the position and size based on the requested percentages
            scrollview_width = window_width * 0.65
            scrollview_height = (window_height - (window_height / 9) - (window_height / 100)) - (window_height/50)
            


            scrollview_pos_x = window_width * 0.31  # from the left side
            scrollview_pos_y = window_height * 0.98  # from the top (remaining height)

            # Create the ScrollView
            scroll_view = ScrollView(
                size_hint=(None, None),
                size=(scrollview_width, scrollview_height),
                pos_hint={'x': scrollview_pos_x / window_width, 'top': scrollview_pos_y/window_height}  # Adjust positions
            )


            # Create the Label for the verse
            verse_label = Label(
                text=self.scripture,  # Add the scripture text here
                font_size=f'{window_width/44}dp',
                size_hint_y=None,  # Make the label grow vertically
                text_size=(scrollview_width, None),  # Text wraps at the width of the scroll view
                halign='left',
                valign='top',
                color=(1, 1, 1, 1)  # Adjust text color if necessary
            )

            # Schedule the height adjustment to happen after the label is rendered
            def update_height(*args):
                verse_label.height = verse_label.texture_size[1]
                print(f"Updated verse label height: {verse_label.height}")

            # Run the update_height function once the current frame is finished
            Clock.schedule_once(update_height, 0)


            # Add the label to the scrollview
            scroll_view.add_widget(verse_label)
            self.layout.add_widget(scroll_view)
            self.current_page_content.append(scroll_view)


    def select_search(self, instance, touch, _pass):
        window_width = Window.width
        window_height = Window.height
        if instance.collide_point(touch.x, touch.y) or _pass:
            self.clear_page_content()
            self.update_selected_icon(self.search_icon, "Search")
            self.search_input = TextInput(
                hint_text="Type a Bible verse",
                size_hint=(1, None),
                height=window_width/16,
                pos_hint={'x': 0, 'top': 0.99},
                multiline=False,
                background_color=(0.66, 0.64, 0.64, 1),  # RGB for #a8a4a4
                foreground_color=(0, 0, 0, 1),
                padding=(10, 10),
                cursor_color=(0, 0, 0, 1),
                cursor_width=1,
                font_size=window_width/32  # Change this value to set the font size
            )
            self.search_input.bind(on_text_validate=self.on_enter_search)
            self.layout.add_widget(self.search_input)
            self.current_page_content.append(self.search_input)


    def update_selected_icon(self, selected_icon, page_name):
        # Reset all icons to default state
        self.home_icon.source = 'homeIco-d.png'
        self.start_icon.source = 'startIco-d.png'
        self.search_icon.source = 'searchIco-d.png'

        # Set the selected icon to active state
        selected_icon.source = selected_icon.source.replace('d.png', 's.png')

    def on_enter_search(self, instance):
        verseL = instance.text  # Get the input verse reference

        # Placeholder for actual Bible lookup logic
        self.scripture = self.search_verse(verseL)
        # print(self.scripture)

        # Create a dummy touch object (simulated)
        dummy_touch = Widget()  # We just need an empty widget to pass as touch
        dummy_touch.x = 0  # Dummy position, as Kivy won't use this for this case
        dummy_touch.y = 0  # Dummy position

        # Call select_start with the dummy touch and instance, but ensure the icon is correctly selected
        self.select_start(self.start_icon, dummy_touch, True)

    def empty_function(self, instance):
        # Empty function for the button
        print("Empty Function")

    def search_verse(self, reference):
        import requests
        url = f"https://bible-api.com/{reference}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            
            # Parse the JSON response
            data = response.json()
            self.reference = reference
            # Get verse text and reference
            verse_text = data.get("text", "Verse not found.")
            # print(f"{reference}: {verse_text}")
            return verse_text
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the verse: {e}")


if __name__ == '__main__':
    MyApp().run()

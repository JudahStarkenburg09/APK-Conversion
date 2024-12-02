from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.metrics import sp  # Import sp for scalable pixel
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.metrics import sp  # Import sp for scalable pixel
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import re, random, string
try:
    from bs4 import BeautifulSoup
except ImportError:
    from subprocess import call
    call(['pip', 'install', 'beautifulsoup4'])
    from bs4 import BeautifulSoup

class ClickableLabel(ButtonBehavior, Label):
    # Add a property for font size
    font_size_ratio = NumericProperty(1)  # Adjust this ratio as needed

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind the font_size to the widget's height
        self.bind(size=self.update_font_size)

    def update_font_size(self, *args):
        # Adjust font size relative to the widget's height
        self.font_size = self.height * self.font_size_ratio

class SmallerClickableLabel(ButtonBehavior, Label):
    # Add a property for font size
    font_size_ratio = NumericProperty(0.6)  # Adjust this ratio as needed

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind the font_size to the widget's height
        self.bind(size=self.update_font_size)

    def update_font_size(self, *args):
        # Adjust font size relative to the widget's height
        self.font_size = self.height * self.font_size_ratio

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

class MainAppScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scripture="Search to choose your piece of scripture"
        self.reference=""
        self.current_sentence_index = 0
        self.defVersion = "ESV"
        self.version = "ESV" # Default Version
        self.selected_version = "ESV"
        self.superscript_dict = {
            "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
            "10": "¹⁰", "11": "¹¹", "12": "¹²", "13": "¹³", "14": "¹⁴", "15": "¹⁵", "16": "¹⁶", "17": "¹⁷", "18": "¹⁸", "19": "¹⁹",
            "20": "²⁰", "21": "²¹", "22": "²²", "23": "²³", "24": "²⁴", "25": "²⁵", "26": "²⁶", "27": "²⁷", "28": "²⁸", "29": "²⁹",
            "30": "³⁰", "31": "³¹", "32": "³²", "33": "³³", "34": "³⁴", "35": "³⁵", "36": "³⁶", "37": "³⁷", "38": "³⁸", "39": "³⁹",
            "40": "⁴⁰", "41": "⁴¹", "42": "⁴²", "43": "⁴³", "44": "⁴⁴", "45": "⁴⁵", "46": "⁴⁶", "47": "⁴⁷", "48": "⁴⁸", "49": "⁴⁹",
            "50": "⁵⁰", "51": "⁵¹", "52": "⁵²", "53": "⁵³", "54": "⁵⁴", "55": "⁵⁵", "56": "⁵⁶", "57": "⁵⁷", "58": "⁵⁸", "59": "⁵⁹",
            "60": "⁶⁰", "61": "⁶¹", "62": "⁶²", "63": "⁶³", "64": "⁶⁴", "65": "⁶⁵", "66": "⁶⁶", "67": "⁶⁷", "68": "⁶⁸", "69": "⁶⁹",
            "70": "⁷⁰", "71": "⁷¹", "72": "⁷²", "73": "⁷³", "74": "⁷⁴", "75": "⁷⁵", "76": "⁷⁶", "77": "⁷⁷", "78": "⁷⁸", "79": "⁷⁹",
            "80": "⁸⁰", "81": "⁸¹", "82": "⁸²", "83": "⁸³", "84": "⁸⁴", "85": "⁸⁵", "86": "⁸⁶", "87": "⁸⁷", "88": "⁸⁸", "89": "⁸⁹",
            "90": "⁹⁰", "91": "⁹¹", "92": "⁹²", "93": "⁹³", "94": "⁹⁴", "95": "⁹⁵", "96": "⁹⁶", "97": "⁹⁷", "98": "⁹⁸", "99": "⁹⁹",
            "100": "¹⁰⁰", "101": "¹⁰¹", "102": "¹⁰²", "103": "¹⁰³", "104": "¹⁰⁴", "105": "¹⁰⁵", "106": "¹⁰⁶", "107": "¹⁰⁷", "108": "¹⁰⁸", 
            "109": "¹⁰⁹", "110": "¹¹⁰", "111": "¹¹¹", "112": "¹¹²", "113": "¹¹³", "114": "¹¹⁴", "115": "¹¹⁵", "116": "¹¹⁶", "117": "¹¹⁷", 
            "118": "¹¹⁸", "119": "¹¹⁹", "120": "¹²⁰", "121": "¹²¹", "122": "¹²²", "123": "¹²³", "124": "¹²⁴", "125": "¹²⁵", "126": "¹²⁶", 
            "127": "¹²⁷", "128": "¹²⁸", "129": "¹²⁹", "130": "¹³⁰", "131": "¹³¹", "132": "¹³²", "133": "¹³³", "134": "¹³⁴", "135": "¹³⁵", 
            "136": "¹³⁶", "137": "¹³⁷", "138": "¹³⁸", "139": "¹³⁹", "140": "¹⁴⁰", "141": "¹⁴¹", "142": "¹⁴²", "143": "¹⁴³", "144": "¹⁴⁴", 
            "145": "¹⁴⁵", "146": "¹⁴⁶", "147": "¹⁴⁷", "148": "¹⁴⁸", "149": "¹⁴⁹", "150": "¹⁵⁰", "151": "¹⁵¹", "152": "¹⁵²", "153": "¹⁵³", 
            "154": "¹⁵⁴", "155": "¹⁵⁵", "156": "¹⁵⁶", "157": "¹⁵⁷", "158": "¹⁵⁸", "159": "¹⁵⁹", "160": "¹⁶⁰", "161": "¹⁶¹", "162": "¹⁶²", 
            "163": "¹⁶³", "164": "¹⁶⁴", "165": "¹⁶⁵", "166": "¹⁶⁶", "167": "¹⁶⁷", "168": "¹⁶⁸", "169": "¹⁶⁹", "170": "¹⁷⁰", "171": "¹⁷¹", 
            "172": "¹⁷²", "173": "¹⁷³", "174": "¹⁷⁴", "175": "¹⁷⁵", "176": "¹⁷⁶"
        }
        print("In Main Screen")
        self.build()

    def go_to_fill_in_the_blank(self, instance):
        # Set the scripture before switching to FillInTheBlankScreen
        fill_in_blank_screen = self.manager.get_screen('fill_in_the_blank')
        fill_in_blank_screen.set_verse(self.scripture)  # Passing the scripture

        # Switch to FillInTheBlankScreen
        self.manager.current = 'fill_in_the_blank'

    def read_verse_by_sentence(self):
        self.clear_page_content()
        self.update_selected_icon(self.start_icon, "Read Mode")

        # Split the scripture into sentences
        sentences = re.split(r'\.\s|"(?=\s|$)', self.scripture)
        self.current_sentence_index = 0

        # Add the "Previous" label
        prev_label = Label(
            text="< Previous",
            font_size='14sp',
            color=(1, 1, 1, 0.7),  # Slightly transparent white
            size_hint=(None, None),
            size=(Window.width * 0.3, 30),
            pos=(20, Window.height - 50),  # Top-left corner
            halign='left',
            valign='middle'
        )
        prev_label.text_size = prev_label.size  # Ensure proper text wrapping
        self.layout.add_widget(prev_label)
        self.current_page_content.append(prev_label)

        # Add the "Next" label
        next_label = Label(
            text="Next >",
            font_size='14sp',
            color=(1, 1, 1, 0.7),  # Slightly transparent white
            size_hint=(None, None),
            size=(Window.width * 0.3, 30),
            pos=(540, Window.height - 50),  # Top-right corner
            halign='right',
            valign='middle'
        )
        next_label.text_size = next_label.size  # Ensure proper text wrapping
        self.layout.add_widget(next_label)
        self.current_page_content.append(next_label)

        # Add the back button
        back_button = Button(
            text="Back",
            font_size='14sp',
            size_hint=(None, None),
            size=(100, 40),  # Set the button size
            pos_hint={'center_x': 0.5, 'top': 1},  # Centered at the top
        )
        back_button.bind(on_press=lambda instance: self.call_start_no_exceptions(instance))  
        self.layout.add_widget(back_button)
        self.current_page_content.append(back_button)

        # Display the first sentence
        self.sentence_label2 = Label(
            text=re.sub(r'\n', '', sentences[self.current_sentence_index]),
            font_size='18sp',
            font_name='noto-sans.ttf',
            size_hint=(1, None),  # Make sure height adjusts to content
            height=Window.height * 0.2,  # Adjust this to give enough space
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            halign='center',
            valign='middle',
        )
        self.sentence_label2.text_size = (Window.width * 0.8, None)  # Adjust width to make sure it wraps correctly

        # Ensure the Label wraps text and respects the layout
        self.layout.add_widget(self.sentence_label2)
        self.current_page_content.append(self.sentence_label2)

        # Add a touchable red rectangle on the left half
        left_rectangle = Widget(
            size_hint=(None, None),
            size=(Window.width * 0.5, Window.height),  # Occupy the left half
            pos_hint={'x': 0, 'top': 1},  # Positioned at the top left corner
            y=70
        )
        with left_rectangle.canvas:
            Color(1, 0, 0, 0)  # Red color
            self.rect_left = Rectangle(size=left_rectangle.size, pos=left_rectangle.pos)

        # Add a touchable blue rectangle on the right half
        right_rectangle = Widget(
            size_hint=(None, None),
            size=(Window.width * 0.5, Window.height),  # Occupy the right half
            pos=(600, 70)  # Positioned at the top right corner
        )
        with right_rectangle.canvas:
            Color(0, 0, 1, 0)  # Blue color
            self.rect_right = Rectangle(size=right_rectangle.size, pos=right_rectangle.pos)

        # Add both rectangles to the layout
        self.layout.add_widget(left_rectangle)
        self.layout.add_widget(right_rectangle)
        self.current_page_content.append(left_rectangle)
        self.current_page_content.append(right_rectangle)

        # Add a touch listener to navigate between sentences
        def navigate_sentences(instance, touch):
            try:
                if left_rectangle.collide_point(touch.x, touch.y):
                    if self.current_sentence_index > 0:
                        self.current_sentence_index -= 1
                        self.sentence_label2.text = sentences[self.current_sentence_index]
                elif right_rectangle.collide_point(touch.x, touch.y):
                    if self.current_sentence_index < len(sentences) - 1:
                        self.current_sentence_index += 1
                        self.sentence_label2.text = sentences[self.current_sentence_index]
            except IndexError:
                try:
                    self.sentence_label2.text = sentences[self.current_sentence_index]
                except IndexError:
                    self.sentence_label2.text = "Something went wrong. Please try again."

        self.layout.bind(on_touch_down=navigate_sentences)

    def show_error_popup(self, error_message):
        # Create a simple popup to display the error message
        content = Button(text="OK", size_hint=(None, None), size=(200, 100))
        popup = Popup(
            title="Error",
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False
        )
        content.bind(on_press=popup.dismiss)  # Close popup when "OK" is pressed

        # Show the error message inside the popup
        error_label = Label(text=f"An error occurred:\n{error_message}", font_size='18sp')
        popup.content = error_label  # Replace content with the error label
        popup.open()

    def build(self):
        self.layout = FloatLayout()
        self.current_page_content = []
        self.rect = None  # Add a variable to track the rectangle

        # Add the main widget (rectangle)
        self.layout.add_widget(MyWidget())

        # Create icons
        self.home_icon = Image(source='homeIco-s.png', size_hint=(0.15, 0.15), pos_hint={'center_x': 0.5, 'y': -0.01})
        self.start_icon = Image(source='startIco-d.png', size_hint=(0.15, 0.15), pos_hint={'center_x': 0.2, 'y': -0.01})
        self.search_icon = Image(source='searchIco-d.png', size_hint=(0.15, 0.15), pos_hint={'center_x': 0.8, 'y': -0.01})


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

        self.add_widget(self.layout)

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

    def methods_overlay(self):
        self.methodsTitle = ClickableLabel(
            text="Choose your method",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.88},
            font_name='impact.ttf',
        )

        self.layout.add_widget(self.methodsTitle)
        self.current_page_content.append(self.methodsTitle)

        # Create and add the button
        # Create and add the clickable text labels
        read = ClickableLabel(
            text="Read",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.72},
            font_name='impact.ttf',
            color=(1, 1, 1, 0.8)
        )

        speech = ClickableLabel(
            text="Speech",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.59},
            font_name='impact.ttf',
            color=(1, 1, 1, 0.8)
        )

        fill_blanks = ClickableLabel(
            text="Fill Blanks",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.46},
            font_name='impact.ttf',
            color=(1, 1, 1, 0.8)
        )

        audio = ClickableLabel(
            text="Audio",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.33},
            font_name='impact.ttf',
            color=(1, 1, 1, 0.8)
        )

        back = ClickableLabel(
            text="Back",
            size_hint=(0.055, 0.055),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            font_name='impact.ttf',
            color=(1, 1, 1, 0.8)
        )


        # Bind the button to the empty function
        read.bind(on_touch_down=lambda instance, touch: self.read_verse_by_sentence() if instance.collide_point(touch.x, touch.y) else None)
        speech.bind(on_press=self.empty_function)
        fill_blanks.bind(on_release=self.go_to_fill_in_the_blank)
        audio.bind(on_press=self.empty_function)
        back.bind(on_touch_down=self.overlay_button_back_pressed)


        self.layout.add_widget(read)
        self.layout.add_widget(speech)
        self.layout.add_widget(fill_blanks)
        self.layout.add_widget(audio)
        self.layout.add_widget(back)

        self.current_page_content.append(read)
        self.current_page_content.append(speech)
        self.current_page_content.append(fill_blanks)
        self.current_page_content.append(audio)
        self.current_page_content.append(back)

        with self.layout.canvas.before:
            Color(0.66, 0.64, 0.64, 0.25)  # Set your desired color (RGB values between 0 and 1)
            self.rect = Rectangle(
                pos=(0, 0),  # bottom-left corner
                size=(Window.width, Window.height)
            )

    def overlay_button_pressed(self, instance, touch):
        # Check if the touch is within the bounds of the instance
        if instance.collide_point(*touch.pos):
            # Clear the current page content
            self.clear_page_content()

            # After clearing, call methods_overlay to add the new content
            self.methods_overlay()
            return True  # Return True to indicate the event was handled

        return False  # Return False if the touch is not within the widget bounds

    def overlay_button_back_pressed(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Clear the current page content
            self.clear_page_content()

            # After clearing, call methods_overlay to add the new content
            self.select_start(self.start_icon, instance, True)

        return False

    def call_search(self, instance, touch):
        # Check if the touch is within the bounds of the instance
        if instance.collide_point(*touch.pos):

            self.clear_page_content()

            self.select_search(instance, touch, True)

    def call_start_no_exceptions(self, instance):
        # Call select_start with _pass set to True
        self.select_start(instance=instance, touch=None, _pass=True)

    def select_start(self, instance, touch, _pass):
        window_width = Window.width
        window_height = Window.height

        # Check if the touch is valid or the _pass flag is True
        if _pass or (touch and instance.collide_point(touch.x, touch.y)):
            self.clear_page_content()
            self.update_selected_icon(self.start_icon, "Start")

            # Get the width and height of the window
            print(f"{window_width} + {window_height}")

            # Variables to represent percentage distances from the window's edges
            from_left = 0.02
            from_right = 0.02
            from_top = 0.25
            from_bottom = 0.12

            # Calculate the width and height based on the distances from the edges
            scrollview_width = window_width * (1 - from_left - from_right)
            scrollview_height = window_height * (1 - from_top - from_bottom)

            # Calculate the position (x and y)
            scrollview_pos_x = window_width * from_left
            scrollview_pos_y = window_height * (1 - from_top)  # Position from the top edge

            # Create the ScrollView
            scroll_view = ScrollView(
                size_hint=(None, None),
                size=(scrollview_width, scrollview_height),
                pos_hint={'x': scrollview_pos_x / window_width, 'top': scrollview_pos_y / window_height}
            )

            # Create the Label for the verse
            verse_label = Label(
                text=self.scripture,  # Add the scripture text here
                font_size=f'{window_width/44}sp',
                font_name='noto-sans.ttf',
                size_hint_y=None,  # Make the label grow vertically
                text_size=(scrollview_width, None),  # Text wraps at the width of the scroll view
                halign='left',
                valign='top',
                color=(1, 1, 1, 1),  # Adjust text color if necessary
            )

            referenceText = ClickableLabel(text=f"{self.reference}",
                    size_hint=(0.0315, 0.0415),
                    color=(1, 1, 1, 1), 
                    pos_hint={'center_x': 0.275, 'center_y': 0.8})


            memorize_button = Image(source='button1-d.png',
                    size_hint=(0.35, 0.125),  # Width and height as a percentage of the parent
                    pos_hint={'center_x': 0.25, 'center_y': 0.925})  # Position relative to parent center

            # Bind the overlay button to the new function
            memorize_button.bind(on_touch_down=self.overlay_button_pressed)

            memorize_text = SmallerClickableLabel(text="Memorize",
                                size_hint=(0.0325, 0.0425),
                                color=(0, 0, 0, 1),
                                pos_hint={'center_x': 0.25, 'center_y': 0.925})
            
            re_search_button = Image(source='button1-d.png',
                    size_hint=(0.35, 0.125),  # Width and height as a percentage of the parent
                    pos_hint={'center_x': 0.75, 'center_y': 0.925})  # Position relative to parent center

            # Bind the overlay button to the new function
            re_search_button.bind(on_touch_down=lambda instance, touch: self.call_search(instance, touch))

            re_search_text = SmallerClickableLabel(text="New Verse",
                                size_hint=(0.0325, 0.0425),
                                color=(0, 0, 0, 1),
                                pos_hint={'center_x': 0.75, 'center_y': 0.925})
            
            # Schedule the height adjustment to happen after the label is rendered
            def update_height(*args):
                verse_label.height = verse_label.texture_size[1]
                print(f"Updated verse label height: {verse_label.height}")


            # Run the update_height function once the current frame is finished
            Clock.schedule_once(update_height, 0)

            # Add the label to the scrollview
            scroll_view.add_widget(verse_label)

            memorize_text.bind(on_touch_down=self.overlay_button_pressed)

            self.layout.add_widget(memorize_button)
            self.layout.add_widget(referenceText)
            self.layout.add_widget(re_search_button)
            self.layout.add_widget(scroll_view)
            self.layout.add_widget(memorize_text)
            self.layout.add_widget(re_search_text)
            self.current_page_content.append(scroll_view)
            self.current_page_content.append(referenceText)
            self.current_page_content.append(memorize_text)
            self.current_page_content.append(re_search_text)
            self.current_page_content.append(memorize_button)
            self.current_page_content.append(re_search_button)

    def select_search(self, instance, touch, _pass):
        window_width = Window.width
        window_height = Window.height
        if instance.collide_point(touch.x, touch.y) or _pass:
            self.clear_page_content()
            self.update_selected_icon(self.search_icon, "Search")
            self.search_input = TextInput(
                hint_text="Search for a verse",
                size_hint=(1, None),
                size_hint_x=.877,
                height=dp(50),  # Adjust the dp value for a consistent height across devices
                pos_hint={'x': 0, 'top': 0.99},
                multiline=False,
                background_color=(0.66, 0.64, 0.64, 1),  # RGB for #a8a4a4
                foreground_color=(0, 0, 0, 1),
                padding=(dp(10), dp(10)),
                cursor_color=(0, 0, 0, 1),
                cursor_width=3,
                font_size=sp(25)  # Use sp for font size to ensure it scales with DPI
            )

            self.switch_versions = Image(source='adjust.png',
                size_hint=(0.115, 0.115),  # Width and height as a percentage of the parent
                pos_hint={'center_x': 0.935, 'center_y': 0.9605})  # Position relative to parent center
            
            self.switch_versions.bind(on_touch_down=lambda instance, touch: self.set_version(instance, touch))
            
            self.layout.add_widget(self.switch_versions)
            self.search_input.bind(on_text_validate=self.on_enter_search)
            self.layout.add_widget(self.search_input)
            self.current_page_content.append(self.search_input)
            self.current_page_content.append(self.switch_versions)

    def set_version(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Touch detected on the version selection screen.")
            self.clear_page_content()

            # Create clickable labels for versions
            version_labels = [
                {"text": "ESV", "pos_y": 0.92},
                {"text": "NKJV", "pos_y": 0.79},
                {"text": "MSG", "pos_y": 0.66},
                {"text": "RV09", "pos_y": 0.53},
                {"text": "Select", "pos_y": 0.27},  # Submit button
            ]

            # Create a list to store the clickable labels
            self.version_widgets = []


            def label_click(instance, touch, version):
                print(f"Label clicked: {version}")

                # Only proceed if the touch is within the bounds of the version label
                if instance.collide_point(*touch.pos):
                    print(f"Touch position: {touch.pos}")
                    # If the label clicked is already the selected one, unselect it
                    if self.selected_version == version:
                        print(f"Unselecting {version}.")
                        # Reset the color of the clicked label and clear the selection
                        instance.color = (1, 1, 1, 0.6)
                        self.selected_version = None
                    else:
                        # Reset all labels to their normal color
                        for label in self.version_widgets:
                            label.color = (1, 1, 1, 0.6)  # Reset all to white

                        instance.color = (1, 1, 1, 1)
                        # Save the selected version
                        self.selected_version = version

            # Create and add the clickable labels to the layout
            for version in version_labels:
                version_label = ClickableLabel(
                    text=version["text"],
                    size_hint=(0.055, 0.055),
                    pos_hint={'center_x': 0.5, 'center_y': version["pos_y"]},
                    font_name='impact.ttf',
                    color=(1, 1, 1, 0.6)  # Default color
                )

                if version["text"] == self.selected_version:
                    version_label.color = (1, 1, 1, 1)
                    self.selected_version = self.selected_version

                # Only bind the click event to labels if no version is selected yet
                if version["text"] != "Select":
                    version_label.bind(on_touch_down=lambda instance, touch, version=version["text"]: label_click(instance, touch, version))

                # Add the label to the layout and the list of widgets
                self.layout.add_widget(version_label)
                self.current_page_content.append(version_label)
                self.version_widgets.append(version_label)

            # Create the "Select" button for submitting the version choice
            select_button = ClickableLabel(
                text="Select",
                size_hint=(0.055, 0.055),
                pos_hint={'center_x': 0.5, 'center_y': 0.27},
                font_name='impact.ttf',
                color=(0.5, 0.5, 0.5, 0.8)  # Initially disabled (gray)
            )

            # Only bind the select action if a version has been selected
            def call_select_search(instance, touch):
                if instance.collide_point(*touch.pos):
                    print(f"================\nSelected {self.selected_version}\n================ ")
                    self.version = self.selected_version
                    self.select_search(instance, touch, _pass=True)
            select_button.bind(on_touch_down=lambda instance, touch: call_select_search(instance, touch))

            # Debug print to check button status
            if self.selected_version:
                print("A version is selected, enabling the 'Select' button.")
                select_button.color = (1, 1, 1, 0.8)  # Enable color (white)
            else:
                print("No version selected, 'Select' button remains disabled.")

            # Add the "Select" button to the layout
            self.layout.add_widget(select_button)
            self.current_page_content.append(select_button)

            # Add the background color to the layout
            with self.layout.canvas.before:
                Color(0.66, 0.64, 0.64, 0.25)  # Set your desired color (RGB values between 0 and 1)
                self.rect = Rectangle(
                    pos=(0, 0),  # bottom-left corner
                    size=(Window.width, Window.height)
                )

    def update_selected_icon(self, selected_icon, page_name):
        # Reset all icons to default state
        self.home_icon.source = 'homeIco-d.png'
        self.start_icon.source = 'startIco-d.png'
        self.search_icon.source = 'searchIco-d.png'

        # Set the selected icon to active state
        selected_icon.source = selected_icon.source.replace('d.png', 's.png')

    def on_enter_search(self, instance):
        try:
            verseL = instance.text  # Get the input verse reference
            self.scripture = self.search_verse(verseL)
            # Proceed as normal with the search result
            self.select_start(self.start_icon, instance, True)

        except Exception as e:
            # Catch any other unexpected errors
            self.show_error_popup(f"An unexpected error occurred: {str(e)}")

    def empty_function(self, instance):
        # Empty function for the button
        print("Empty Function")

    def search_verse(self, reference):
        import get_verse, re

        resultList, resultStr = get_verse.search_verse(self.version, reference)
        resultStr = re.sub(r"(\d+): ", lambda match: self.superscript_dict.get(match.group(1), match.group(1) + ": "), resultStr)
        return resultStr
        
# ---------------------------------------------------------------------------------------------------------

class FillInTheBlankScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scripture = ""  # Placeholder for scripture
        self.layout = FloatLayout()  # Use FloatLayout to enable pos_hint functionality
        self.current_index = 0  # Initialize sentence index
        self.sentences = []  # Will store sentences after splitting the scripture
        self.selected_level = {}  # Initialize selected_level here
        self.initialize_levels()  # Initialize the difficulty levels when screen is created
        print("Screen initialized.")  # Debugging to confirm initialization
        self.add_widget(self.layout)  # Add layout to the screen once during initialization

    def set_verse(self, verse):
        """Set the scripture passed from MainAppScreen."""
        self.scripture = verse
        print(f"Verse received: {self.scripture}")  # Debugging to check if the verse is passed
        
        # Split the verse into sentences and update layout after receiving the verse
        self.sentences = self.split_into_sentences(self.scripture)  
        print(f"Sentences: {self.sentences}")  # Debugging to check if the sentences are split correctly
        
        # After setting the verse, now update the layout
        self.update_sentence_layout()  # Ensure the layout is updated after the verse is set

    def initialize_levels(self):
        """Initialize the difficulty levels (easy, medium, hard)."""
        easy_factor = 0.3
        medium_factor = 0.45
        hard_factor = 0.85

        # Function to calculate the number of blanks based on the difficulty and word count
        def calculate_blanks(word_count, difficulty_factor):
            return max(1, int(word_count * difficulty_factor))

        # Example for sentences with varying word counts
        self.lvl_easy = {i: calculate_blanks(i, easy_factor) for i in range(2, 58)}
        self.lvl_medium = {i: calculate_blanks(i, medium_factor) for i in range(2, 58)}
        self.lvl_hard = {i: calculate_blanks(i, hard_factor) for i in range(2, 58)}
        
        self.selected_level = self.lvl_easy  # Default level is set to easy

    def update_sentence_layout(self):
        """Updates the layout with the current sentence, replacing random words with blanks."""
        print("Updating sentence layout...")  # Debugging to confirm that the layout is being updated
        self.layout.clear_widgets()  # Clear previous widgets
        self.user_inputs = []  # List to store TextInput widgets for comparison
        self.correct_words = []  # List to store the correct words for blanks

        if not self.sentences:  # If no sentences are available, display a fallback message
            self.sentences = ["No scripture chosen."]
        
        # Get the current sentence to display
        self.current_sentence = self.sentences[self.current_index]
        words = self.current_sentence.split()
        self.blank_count = self.selected_level.get(len(words), 1)  # Get the blank count based on the word count
        longest_word_length = max(len(word) for word in words)
        print(f"Words in current sentence: {words}")  # Debugging to check the words in the sentence
        word_length_to_size = {8:80, 9:85, 10:90, 11:95, 12:100, 13: 105, 14: 110, 15: 115, 16:120, 17:125, 18:130, 19:130}
        for i, key in enumerate(word_length_to_size):
            word_length_to_size[key] -= 5
        # Randomly select indices for blanks
        blank_indices = random.sample(range(len(words)), self.blank_count)

        self.line_spacing = dp(60)

        # Create a grid layout for the sentence with blanks
        sentence_layout = GridLayout(cols=4, size_hint=(0.9, None), row_default_height=self.line_spacing , pos_hint={'center_x': 0.6, 'center_y': 0.85})
        sentence_layout.bind(minimum_height=sentence_layout.setter('height'))  # Ensure it wraps correctly
 
        for i, word in enumerate(words):
            if i in blank_indices:
                # Replace the word with a TextInput (blank)
                blank = TextInput(
                    multiline=False,
                    size_hint=(None, None),
                    size=(word_length_to_size.get(longest_word_length, 70), 40),  # Fixed size for blanks
                    background_color=(1, 1, 1, 0.05),
                    font_name = "cour.ttf",
                    cursor_width=3,
                    foreground_color=(1, 1, 1, 1),
                    halign="center",
                    font_size=sp(18)
                )
                blank.bind(on_text_validate=self.next_empty_entry)  # Bind Enter key event
                sentence_layout.add_widget(blank)
                self.user_inputs.append(blank)  # Store the TextInput widget in the list
                self.correct_words.append(word)  # Store the correct word for this blank
            else:
                self.wrap_width = 150  # Define the maximum width for wrapping text
                # Add the word as a label
                label = Label(
                    text=word,
                    size_hint=(None, None),
                    size=(self.wrap_width, 40),  # Dynamically size based on word length
                    halign="center",
                    font_name = "cour.ttf",
                    valign="middle",
                    font_size=sp(18)
                )
                label.bind(size=label.setter('text_size'))  # Ensure text fits inside label
                sentence_layout.add_widget(label)

        self.layout.add_widget(sentence_layout)

        # Add a submit button at the bottom of the layout
        submit_button = Button(
            text="Submit",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        submit_button.bind(on_press=self.submit_answers)
        self.layout.add_widget(submit_button)

        # Add the "Finish Quiz" button
        finish_button = Button(
            text="Finish Quiz",
            size_hint=(0.22, 0.1),  # Adjust the size
            pos_hint={'right': 0.95, 'top': 0.15},  # Position at the bottom-right
            background_color=(0.2, 0.6, 0.2, 1)  # Green background color
        )
        finish_button.bind(on_press=self.finish_quiz)  # Bind the button to the finish_quiz function
        self.layout.add_widget(finish_button)


    def finish_quiz(self, instance):
        """Handles the action when the 'Finish Quiz' button is pressed."""
        print("Quiz Finished!")  # For now, just print a message
        self.manager.current = 'main_app'  # Switch back to MainAppScreen (or handle as needed)

    def split_into_sentences(self, text):
        """Splits the text into a list of sentences."""
        # Initial split using punctuation (periods, exclamation points, question marks)
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        final_sentences = []

        for sentence in sentences:
            words = sentence.split()
            while len(words) > 18:  # Handle sentences longer than 18 words
                # Check for commas in the next 18 words to split
                for i in range(12, min(18, len(words))):
                    if ',' in words[i]:
                        # Split at the comma and adjust
                        final_sentences.append(' '.join(words[:i + 1]).strip(','))
                        words = words[i + 1:]
                        break
                else:
                    # If no comma is found, split at 18 words
                    final_sentences.append(' '.join(words[:18]))
                    words = words[18:]

            # Add any remaining words as a sentence
            if words:
                final_sentences.append(' '.join(words))

        return final_sentences

    def clean_text(self, text):
        """Cleans the text by removing punctuation and trimming whitespaces, ignoring special characters like verse numbers."""
        text = text.strip().lower()  # Remove leading/trailing spaces and convert to lowercase

        # Remove superscript numbers and other non-alphanumeric characters
        text = re.sub(r'[\u00B9\u00B2\u00B3\u00B4\u00B5\u00B6\u00B7\u00B8\u00B9\u00BA\u00BB\u00BC\u00BD\u00BE\u00BF\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5\u00C6\u00C7\u00C8\u00C9\u00CA\u00CB\u00CC\u00CD\u00CE\u00CF\u00D0\u00D1\u00D2\u00D3\u00D4\u00D5\u00D6\u00D7\u00D8\u00D9\u00DA\u00DB\u00DC\u00DD\u00DE\u00DF\u00E0\u00E1\u00E2\u00E3\u00E4\u00E5\u00E6\u00E7\u00E8\u00E9\u00EA\u00EB\u00EC\u00ED\u00EE\u00EF\u00F0\u00F1\u00F2\u00F3\u00F4\u00F5\u00F6\u00F7\u00F8\u00F9\u00FA\u00FB\u00FC\u00FD\u00FE\u00FF\u2010\u2013\u2014\u2018\u2019\u201C\u201D\u2022\u2026\u2032\u2033\u2034\u2035\u2036\u2037\u2038\u2039\u203A\u203B\u203C\u203D\u203E\u203F\u2040\u2041\u2042\u2043\u2044\u2045\u2046\u2047\u2048\u2049\u204A\u204B\u204C\u204D\u204E\u204F\u2050\u2051\u2052\u2053\u2054\u2055\u2056\u2057\u2058\u2059\u205A\u205B\u205C\u205D\u205E\u205F\u2060\u2061\u2062\u2063\u2064\u2065\u2066\u2067\u2068\u2069\u206A\u206B\u206C\u206D\u206E\u206F\u2070\u2071\u2072\u2073\u2074\u2075\u2076\u2077\u2078\u2079\u207A\u207B\u207C\u207D\u207E\u207F\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089]', '', text)
        return ''.join([char for char in text if char not in string.punctuation])  # Remove punctuation

    def submit_answers(self, instance):
        """Submits the answers and checks if correct, then updates the UI."""
        all_correct = True

        for i, user_input in enumerate(self.user_inputs):
            cleaned_input = self.clean_text(user_input.text)  # Get text from TextInput field
            cleaned_correct_word = self.clean_text(self.correct_words[i])

            if cleaned_input == cleaned_correct_word:
                user_input.background_color = (0, 1, 0, 1)  # Green
                user_input.disabled = True
            else:
                all_correct = False

        if all_correct:
            self.show_next_button()

    def show_next_button(self):
        """Displays the Next button when all answers are correct."""
        next_button = Button(
            text="Next",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        next_button.bind(on_press=self.next_sentence)
        self.layout.add_widget(next_button)

    def next_sentence(self, instance):
        """Moves to the next sentence."""
        self.layout.clear_widgets()  # Clear the previous widgets
        self.current_index += 1
        if self.current_index >= len(self.sentences):
            self.current_index = 0  # Loop back to the first sentence if all sentences are used
        self.update_sentence_layout()  # Load the next sentence

    def next_empty_entry(self, instance):
        """Move focus to the next empty entry when Enter is pressed."""
        for i, user_input in enumerate(self.user_inputs):
            if not user_input.text.strip():  # If the current TextInput is empty
                user_input.focus = True
                break

# --------------------------------------------------------------------------------------------------------

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()

        # Add MainAppScreen
        self.main_app_screen = MainAppScreen(name='main_app')
        self.sm.add_widget(self.main_app_screen)

        # Add FillInTheBlankScreen
        self.fill_in_the_blank_screen = FillInTheBlankScreen(name='fill_in_the_blank')
        self.sm.add_widget(self.fill_in_the_blank_screen)

        self.sm.current = 'main_app'  # or 'fill_in_the_blank' for the other screen

        return self.sm



if __name__ == '__main__':
    MyApp().run()

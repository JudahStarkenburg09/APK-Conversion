from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty
try:
    from bs4 import BeautifulSoup
    import lxml
except ImportError:
    from subprocess import call
    call(['pip', 'install', 'beautifulsoup4', 'lxml'])
    from bs4 import BeautifulSoup
    import lxml

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

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scripture="Search to choose your piece of scripture"
        self.reference=""
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
        read.bind(on_press=self.empty_function)
        speech.bind(on_press=self.empty_function)
        fill_blanks.bind(on_press=self.empty_function)
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

    def select_start(self, instance, touch, _pass):
        window_width = Window.width
        window_height = Window.height
        if instance.collide_point(touch.x, touch.y) or _pass:
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
                size_hint_y=None,  # Make the label grow vertically
                text_size=(scrollview_width, None),  # Text wraps at the width of the scroll view
                halign='left',
                valign='top',
                color=(1, 1, 1, 1)  # Adjust text color if necessary
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
                size_hint_x=.883,
                height=dp(50),  # Adjust the dp value for a consistent height across devices
                pos_hint={'x': 0, 'top': 0.99},
                multiline=False,
                background_color=(0.66, 0.64, 0.64, 1),  # RGB for #a8a4a4
                foreground_color=(0, 0, 0, 1),
                padding=(dp(10), dp(10)),
                cursor_color=(0, 0, 0, 1),
                cursor_width=1,
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

    def select_vname(self, ):
        ''

    def set_version(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Touch detected on the version selection screen.")
            self.clear_page_content()

            # Create clickable labels for versions
            version_labels = [
                {"text": "ESV", "pos_y": 0.92},
                {"text": "NKJV", "pos_y": 0.79},
                {"text": "NLT", "pos_y": 0.66},
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
                        instance.color = (1, 1, 1, 0.8)
                        self.selected_version = None
                    else:
                        # Reset all labels to their normal color
                        for label in self.version_widgets:
                            label.color = (1, 1, 1, 0.8)  # Reset all to white
                        # Set the clicked label to blue
                        instance.color = (0, 0, 1, 1)
                        # Save the selected version
                        self.selected_version = version

            # Create and add the clickable labels to the layout
            for version in version_labels:
                version_label = ClickableLabel(
                    text=version["text"],
                    size_hint=(0.055, 0.055),
                    pos_hint={'center_x': 0.5, 'center_y': version["pos_y"]},
                    font_name='impact.ttf',
                    color=(1, 1, 1, 0.8)  # Default color
                )

                if version["text"] == self.selected_version:
                    version_label.color = (0, 0, 1, 1)
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
        


if __name__ == '__main__':
    MyApp().run()
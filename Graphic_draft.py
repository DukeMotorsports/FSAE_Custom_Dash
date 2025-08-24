from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import random
import CAN as CAN

# Display resolution (set for Raspberry Pi 5" display)
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

MAX_RPM = 7000
gears = ["N", "1", "2", "3", "4", "5", "6"]
current_gear_index = 0

# Set window size
Window.size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)


class RaceDash(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = dp(10)
        self.spacing = dp(20)

        # Background color control
        self.bg_color = [0.1, 0.1, 0.1, 1]  # dark gray
        Window.clearcolor = self.bg_color

        # RPM bar
        self.rpm_bar = ThickProgressBar(max=MAX_RPM, value=0, size_hint=(1, None), height=100)
        self.add_widget(self.rpm_bar)

        # Spacer
        self.add_widget(BoxLayout(size_hint_y=None, height=DISPLAY_HEIGHT//4))

        # Gear label (big font)
        self.gear_label = Label(
            text=gears[current_gear_index],
            font_size=200,
            size_hint=(1, None),
            height=250
        )
        self.add_widget(self.gear_label)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, None), height=80, spacing=20, padding=20)
        self.up_button = Button(text="Upshift", on_press=self.upshift)
        self.down_button = Button(text="Downshift", on_press=self.downshift)
        button_layout.add_widget(self.up_button)
        button_layout.add_widget(self.down_button)
        self.add_widget(button_layout)

        # Flash state
        self.flash_state = False

        # Start RPM update loop (30 times per second)
        Clock.schedule_interval(self.update_rpm, 1/30)

    def update_rpm(self, dt):
        # Simulate RPM for now
        rpm_value = random.randint(0, MAX_RPM)
        self.rpm_bar.value = rpm_value
        self.rpm_bar.value_normalized = rpm_value / MAX_RPM
        self.rpm_bar.text = f"{rpm_value} RPM"

        # Flashing effect if RPM >= 80%
        if rpm_value >= 0.8 * MAX_RPM:
            self.flash_state = not self.flash_state
            Window.clearcolor = [1, 0, 0, 1] if self.flash_state else [0.1, 0.1, 0.1, 1]
        else:
            Window.clearcolor = [0.1, 0.1, 0.1, 1]

    def upshift(self, instance):
        global current_gear_index
        if current_gear_index < len(gears) - 1:
            current_gear_index += 1
        self.gear_label.text = gears[current_gear_index]

    def downshift(self, instance):
        global current_gear_index
        if current_gear_index > 0:
            current_gear_index -= 1
        self.gear_label.text = gears[current_gear_index]

class ThickProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0.2, 0.2, 0.2, 1)  # dark gray background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        with self.canvas.after:
            self.fg_color = Color(0, 1, 0, 1)  # green foreground bar
            self.fg_rect = Rectangle(pos=self.pos, size=(0, self.height))

        # Update rectangles when position, size, or value changes
        self.bind(pos=self.update_rects, size=self.update_rects, value=self.update_rects)

    def update_rects(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width * (self.value / self.max), self.height)


class RaceDashApp(App):
    def build(self):
        return RaceDash()


if __name__ == "__main__":
    RaceDashApp().run()

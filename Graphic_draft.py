import dearpygui.dearpygui as dpg
import random

# Display resolution (change if your 5" screen is different)
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

MAX_RPM = 7000
gear = "N"

dpg.create_context()

# Create viewport (app window)
dpg.create_viewport(title="Race Dash", width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, resizable=False)

# Load a big font for the gear number
with dpg.font_registry():
    big_font = dpg.add_font("C:/Windows/Fonts/arial.ttf", 200)  # Adjust path and size if needed

# Create themes for normal & flashing backgrounds
with dpg.theme() as normal_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 20, 255))  # dark gray

with dpg.theme() as warning_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 0, 0, 255))  # bright red
# Function to update gear
def set_gear(value):
    dpg.set_value("Gear Position", value)

# Function to update RPM bar(color rpm bar)
# def update_rpm():
#     rpm_value = random.randint(0, MAX_RPM) / MAX_RPM
#     dpg.set_value("RPM GAUGE", rpm_value)

#     # Color logic
#     if rpm_value < 0.6:
#         color = (0, 255, 0, 255)
#     elif rpm_value < 0.85:
#         color = (255, 255, 0, 255)
#     else:
#         color = (255, 0, 0, 255)
    # dpg.configure_item("RPM GAUGE", overlay=f"{int(rpm_value * MAX_RPM)} RPM")
    # dpg.bind_item_theme("RPM GAUGE", create_bar_theme(color))

flash_state = False
def update_rpm():
    global flash_state
    rpm_value = random.randint(0, MAX_RPM) / MAX_RPM
    dpg.set_value("RPM GAUGE", rpm_value)
    dpg.configure_item("RPM GAUGE", overlay=f"{int(rpm_value*MAX_RPM)} RPM")

    if rpm_value >= 0.8:
        # Toggle flashing effect every update
        flash_state = not flash_state
        if flash_state:
            dpg.bind_item_theme("Main Display", warning_theme)
        else:
            dpg.bind_item_theme("Main Display", normal_theme)
    else:
        dpg.bind_item_theme("Main Display", normal_theme)

# Main dash window
with dpg.window(label="Main Display",
                tag= "Main Display",
                width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT,
                no_resize=True, no_move=True, no_title_bar=True):

    # RPM bar at the very top
    dpg.add_progress_bar(tag="RPM GAUGE", default_value=0, width=DISPLAY_WIDTH-20, height=40, overlay="0 RPM")

    # Spacer to push gear number down vertically
    dpg.add_spacer(height=(DISPLAY_HEIGHT//2) - 150)

    # Centered gear display
    dpg.add_text(gear, tag="Gear Position", indent=(DISPLAY_WIDTH//2) - 60)

    # Buttons for testing
    dpg.add_spacer(height=50)
    dpg.add_button(label="Upshift", callback=lambda: set_gear("1"))
    dpg.add_button(label="Downshift", callback=lambda: set_gear("N"))

# Apply big font to gear number
dpg.bind_item_font("Gear Position", big_font)

# Simulate RPM updates every frame
def rpm_loop(sender, app_data):
    update_rpm()

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda: None)  # Just to create a registry

dpg.setup_dearpygui()
dpg.show_viewport()

# Manual main loop so we can update RPM without freezing
while dpg.is_dearpygui_running():
    update_rpm()
    dpg.render_dearpygui_frame()

dpg.destroy_context()

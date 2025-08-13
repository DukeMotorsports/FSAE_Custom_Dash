import dearpygui.dearpygui as dpg
import random
import time

MAX_RPM = 7000
gear = 0
running = False

dpg.create_context()
dpg.create_viewport(title='RPM GAUGE', width=600, height=300)

def update_rpm():
    rpm_value = random.randint(0, MAX_RPM) / MAX_RPM
    dpg.set_value("RPM GAUGE", rpm_value)

    # Color logic
    if rpm_value < 0.6:
        color = (0, 255, 0, 255)
    elif rpm_value < 0.85:
        color = (255, 255, 0, 255)
    else:
        color = (255, 0, 0, 255)

    dpg.configure_item("RPM GAUGE", overlay=f"{int(rpm_value * MAX_RPM)} RPM")
    dpg.bind_item_theme("RPM GAUGE", create_bar_theme(color))

def create_bar_theme(color):
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, color)
    return theme

def upShift():
    global gear
    gear += 1
    dpg.set_value("Gear Position", str(gear))

def downShift():
    global gear
    if gear > 0:
        gear -= 1
        dpg.set_value("Gear Position", str(gear))

def start_updates():
    global running
    running = True

def stop_updates():
    global running
    running = False

with dpg.window(label="RPM Tester", pos=(0,0), width=550, height=150):
    dpg.add_progress_bar(tag="RPM GAUGE", default_value=0, width=500, height=100, overlay="0 RPM")
    dpg.add_button(label="Start", callback=start_updates)
    dpg.add_button(label="Stop", callback=stop_updates)

with dpg.window(label="Gear Position", pos=(100,200)):
    dpg.add_text(default_value='N', tag="Gear Position")
    dpg.add_button(label="Upshift", callback=upShift)
    dpg.add_button(label="Downshift", callback=downShift)

dpg.setup_dearpygui()
dpg.show_viewport()

# Manual update loop that yields control each frame
while dpg.is_dearpygui_running():
    if running:
        update_rpm()
        time.sleep(0.1)  # control update rate
    dpg.render_dearpygui_frame()

dpg.destroy_context()

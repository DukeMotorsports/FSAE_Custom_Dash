import dearpygui.dearpygui as dpg
import time
import threading

progress_value = 0.0
progress_running = False

def update_progress():
    global progress_value, progress_running
    progress_running = True
    while progress_value < 1.0 and progress_running:
        time.sleep(1)  # wait for 1 second
        progress_value += 0.1
        dpg.set_value("progress_bar", progress_value)

def start_progress():
    global progress_value, progress_running
    if not progress_running:
        progress_value = 0.0
        dpg.set_value("progress_bar", progress_value)
        threading.Thread(target=update_progress, daemon=True).start()

with dpg.window(label="Progress Bar Example", width=400, height=200):
    dpg.add_button(label="Start", callback=start_progress)
    dpg.add_progress_bar(tag="progress_bar", default_value=0.0, width=300)

dpg.start_dearpygui()
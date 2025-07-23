import dearpygui.dearpygui as dpg
import random
import time
MAX_RPM = 7000
rpm = 0.0
# notes: progress bar takes value from 0 to 1
# need to normalize the rpm data so that it's within 0 to 1

dpg.create_context()
dpg.create_viewport(title='RPM GAUGE', width=600, height=300)

# replace with parameter from CAN
def updateRPM():
    rpm = random.randint(0, MAX_RPM)
    rpm /= MAX_RPM
    return rpm
def activate():
    while(True):
        print(updateRPM())
        dpg.set_value("RPM GAUGE", value=updateRPM())
        time.sleep(0.1)
def deactivate():
    dpg.destroy_viewport()
    dpg.destroy_context()

with dpg.window(label="RPM Tester"):
    dpg.add_progress_bar(tag = "RPM GAUGE", default_value=0, width=500, height=100)
    dpg.add_button(label="Start", tag="Start", callback=activate, width=100)
    # dpg.add_button(label="Stop", tag = "Stop", callback=deactivate, width=100)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
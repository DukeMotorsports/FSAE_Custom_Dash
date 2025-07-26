import dearpygui.dearpygui as dpg
import random
import time
MAX_RPM = 7000
rpm = 0.0
gear = 0
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

def upShift():
    gear += 1
    dpg.set_value("Gear Position", value = gear)

def downShift():
    if(gear > 0):
        gear-=1
        dpg.set_value("Gear Position", value = gear)

with dpg.window(label="RPM Tester"):
    dpg.add_progress_bar(tag = "RPM GAUGE", default_value=0, width=500, height=100)
    dpg.add_button(label="Start", tag="Start", callback=activate, width=100)
    # dpg.add_button(label="Stop", tag = "Stop", callback=deactivate, width=100)

with dpg.window(label = "Gear position"):
    dpg.add_text(default_value='N', label="Gear Position", tag="Gear Position")
    dpg.add_button(label = "Upshfit", tag = "Upshift", callback=upShift)
    dpg.add_button(label="Downshift", tag="Downshift", callback=downShift)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
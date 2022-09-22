# The main entry point to the program.
import dearpygui.dearpygui as dpg
from config import Configuration
from context_menu import ContextMenu
from utils import Debug

dpg.create_context()
dpg.show_style_editor()
dpg.enable_docking(dock_space=True)

# add a font registry
with dpg.font_registry():
    default_font = dpg.add_font("assets/fonts/SF-Pro-Text-Thin.otf", 15)
    dpg.add_font("assets/fonts/SF-Pro-Text-Regular.otf", 15)
    dpg.add_font("assets/fonts/SF-Pro-Text-Bold.otf", 15)

config = Configuration()
debug = Debug()

# debug.show_dev_tools()

with dpg.window(label="Main", pos=(0,0)) as main_window:
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

with dpg.window(label="Main2", pos=(0,0)) as main_window:
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
    
context_menu = ContextMenu()
context_menu.show(main_window)

dpg.create_viewport(title=config.APP_TITLE, width=config.APP_WIDTH, height=config.APP_HEIGHT)

dpg.bind_font(default_font)

dpg.show_font_manager()


dpg.setup_dearpygui()
dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
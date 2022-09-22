import dearpygui.dearpygui as dpg
from config import Configuration

class Debug:
    _config = None
    def __init__(self):
        self._config = Configuration()

    def show_dev_tools(self):
        dpg.create_context()

        dpg.show_documentation()
        dpg.show_style_editor()
        dpg.show_debug()
        dpg.show_about()
        dpg.show_metrics()
        dpg.show_font_manager()
        dpg.show_item_registry()

        dpg.create_viewport(title=self._config.APP_TITLE, width=self._config.APP_WIDTH, height=self._config.APP_HEIGHT)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    

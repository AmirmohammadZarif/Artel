import xml.etree.ElementTree as ET

class Settings:
    _root = None
    def __init__(self, config_file):
        tree = ET.parse(config_file)
        self._root = tree.getroot()

    def get_setting(self, setting) -> str:
        for child in self._root:
            if child.attrib['id'] == setting:
                return child.attrib['value']

class Configuration:
    # Local variables
    _settings = None

    # Properties and Configurations
    APP_TITLE = None
    APP_WIDTH = None
    APP_HEIGHT = None

    def __init__(self):
        self._settings = Settings("./configuration.xml")

        self.APP_TITLE = self._settings.get_setting('title')
        self.APP_WIDTH = int(self._settings.get_setting('width'))
        self.APP_HEIGHT = int(self._settings.get_setting('height'))




if __name__ == "__main__":
    setting = Settings("./configuration.xml")
    print(setting.get_setting("title"))
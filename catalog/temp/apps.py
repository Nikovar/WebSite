from django.apps import AppConfig
import catalog.temp.settings as local_settings


class TempConfig(AppConfig):
    name = 'catalog.temp'

    def __init__(self, app_name, app_module):
        AppConfig.__init__(self, app_name, app_module)
        local_settings.APP_PATH = self.path

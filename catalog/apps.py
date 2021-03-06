from django.apps import AppConfig
from . import settings as local_settings


class CatalogConfig(AppConfig):
    name = 'catalog'

    def __init__(self, app_name, app_module):
        AppConfig.__init__(self, app_name, app_module)
        local_settings.APP_PATH = self.path

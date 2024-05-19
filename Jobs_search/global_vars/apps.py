from django.apps import AppConfig
from .globalVariableManager import GlobalVariableManager

class GlobalVarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'global_vars'

    def ready(self):
        # Start the global variable manager thread when the app is ready
        global_var_manager = GlobalVariableManager()
        global_var_manager.start()
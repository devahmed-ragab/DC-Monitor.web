from django.apps import AppConfig


class DcMonitorConfig(AppConfig):
    name = 'dc_monitor_app'

    def ready(self):
        import dc_monitor_app.signals
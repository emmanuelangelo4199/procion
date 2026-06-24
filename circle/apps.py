from django.apps import AppConfig


class CircleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'circle'

    def ready(self):
        # This imports the signals file when Django starts up
        import circle.signals
        
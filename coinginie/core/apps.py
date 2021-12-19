from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coinginie.core'

    def ready(self):
        try:
            import coinginie.core.signals  # noqa F401
        except ImportError:
            pass

from django.apps import AppConfig


class ContractsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coinginie.contracts'

    def ready(self):
        try:
            import coinginie.contracts.signals  # noqa F401
        except ImportError:
            pass

from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coinginie.wallet'

    def ready(self):
        try:
            import coinginie.wallet.signals  # noqa F401
        except ImportError:
            pass

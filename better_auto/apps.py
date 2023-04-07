from django.apps import AppConfig


class BetterAutoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'better_auto'

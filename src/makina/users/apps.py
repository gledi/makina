from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "makina.users"

    def ready(self) -> None:
        import makina.users.signals  # noqa: F401

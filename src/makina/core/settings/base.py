from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environs import Env

env = Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent.parent

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    # django builtins
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # 3rd party apps
    "rest_framework",
    "crispy_forms",
    "crispy_bulma",
    "imagekit",
    "fontawesomefree",
    # local apps
    "makina.pages",
    "makina.vehicles",
    "makina.blog",
    "makina.users",
    "makina.shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "makina.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "makina.shop.context_processors.cart_total_items",
            ],
        },
    },
]

WSGI_APPLICATION = "makina.core.wsgi.application"


DATABASES = {"default": env.dj_db_url("DATABASE_URL")}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en-US", _("English (US)")),
    ("sq-AL", _("Albanian")),
    ("it-IT", _("Italian")),
]
LOCALE_PATHS = [BASE_DIR / "locales"]
USE_I18N = True

TIME_ZONE = "UTC"
USE_TZ = True


STATIC_ROOT = ROOT_DIR / "static"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


MEDIA_URL = "media/"
MEDIA_ROOT = ROOT_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "registration@makina.al"

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)
CRISPY_TEMPLATE_PACK = "bulma"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if DEBUG else "WARNING",
    },
}

STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env.str("STRIPE_SECRET_KEY")

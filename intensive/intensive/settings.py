from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv("SECRET_KEY", "NOTSECRET")

DEBUG = getenv("DEBUG", "false").lower() == "true"

if DEBUG:
    ALLOWED_HOSTS = "*"
else:
    ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost")
ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")

REVERSE_REQUEST_COUNT = int(getenv("REVERSE_REQUEST_COUNT", "0"))

GRAPH_APPS = getenv("GRAPH_APPS", "")
GRAPH_APPS = GRAPH_APPS.split(",") if GRAPH_APPS else ""

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
    "feedback.apps.FeedbackConfig",
    "users.apps.UsersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "intensive.middleware.ReverseMiddleware",
]

if DEBUG:
    # django debug toolbar is needed only in developments
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

if GRAPH_APPS:
    INSTALLED_APPS.append("django_extensions")
    GRAPH_MODELS = {
        "group_models": True,
        "app_labels": GRAPH_APPS,
    }

ROOT_URLCONF = "intensive.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "intensive.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

IS_USER_ACTIVE = getenv("IS_USER_ACTIVE", "false").lower() == "true"
IS_USER_ACTIVE = True if DEBUG else IS_USER_ACTIVE

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "users.backends.AuthenticationEmailBackend",
]

LOCALE_PATHS = [BASE_DIR / "locale"]
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static_dev"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


FEEDBACK_EMAIL = getenv("FEEDBACK_EMAIL", "example@email.com")
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

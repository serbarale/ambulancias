"""Test settings inside the ambulancias app package for pytest-django.
"""
SECRET_KEY = "test-secret-key"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "ambulancias",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

USE_TZ = True

ROOT_URLCONF = "ambulancias.urls"

MIDDLEWARE = []

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

ALLOWED_HOSTS = ["testserver"]

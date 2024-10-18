from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "@s$j92j-_t0500=*2)&(s^b38xszk!g)z#cjz&_98#!1d#ta=n"

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://hpdev.beyond-board.me','http://127.0.0.1', 'http://192.168.1.107:3000','https://hpdev.beyond-board.me/en/']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

OPENAI_API_KEY = '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'
WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass

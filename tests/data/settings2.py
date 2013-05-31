CELERY_RESULT_BACKEND = 'foo'

CACHES = {'default': {'BACKEND': 'bar'}}
INSTALLED_APPS = ('zap', 'qux')
USE_TZ = False

EXTRA2 = 2


def custom_show_toolbar():
    return False  # Always show toolbar, for example purposes only.


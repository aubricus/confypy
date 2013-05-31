import os
from confypy import Config
from confypy import Location


def test_locations_python_first():
    config = Config()
    config.locations = [Location.from_python('tests.data.settings1')]

    assert config.data.CELERY_RESULT_BACKEND == 'amqp'

    assert config.data.CACHES['default']['BACKEND'] == \
    'django.core.cache.backends.memcached.MemcachedCache'

    assert 'south' in config.data.INSTALLED_APPS
    assert config.data.USE_TZ == True
    assert config.data.custom_show_toolbar() == True


def test_locations_python_first_env():
    os.environ['TEST_SETTINGS'] = 'tests.data.settings1'

    config = Config()
    config.locations = [Location.from_env_python('TEST_SETTINGS')]

    assert config.data.CELERY_RESULT_BACKEND == 'amqp'

    assert config.data.CACHES['default']['BACKEND'] == \
    'django.core.cache.backends.memcached.MemcachedCache'

    assert 'south' in config.data.INSTALLED_APPS
    assert config.data.USE_TZ == True
    assert config.data.custom_show_toolbar() == True


def test_locations_python_first_multi():
    os.environ['TEST_SETTINGS'] = 'tests.data.settings2'

    config = Config()
    config.locations = [
    Location.from_env_python('TEST_SETTINGS'),
    Location.from_python('tests.data.settings1')]

    assert config.data.CELERY_RESULT_BACKEND == 'foo'

    assert config.data.CACHES['default']['BACKEND'] == 'bar'

    assert 'zap' in config.data.INSTALLED_APPS
    assert config.data.USE_TZ == False
    assert config.data.custom_show_toolbar() == False


def test_locations_python_first_multi_fail():
    os.environ['TEST_SETTINGS'] = 'tests.data.notfound'

    config = Config()
    config.locations = [
    Location.from_env_python('TEST_SETTINGS'),
    Location.from_python('tests.data.settings1')]

    assert config.data.CELERY_RESULT_BACKEND == 'amqp'

    assert config.data.CACHES['default']['BACKEND'] == \
    'django.core.cache.backends.memcached.MemcachedCache'

    assert 'south' in config.data.INSTALLED_APPS
    assert config.data.USE_TZ == True
    assert config.data.custom_show_toolbar() == True


def test_locations_python_first_multi_defaults():
    os.environ['TEST_SETTINGS'] = 'tests.data.notfound1'

    config = Config(defaults={
        'name': 'lorem',
        'occupation': 'ipsum',
        'Sound': 'latin'})

    config.locations = [
    Location.from_env_python('TEST_SETTINGS'),
    Location.from_python('tests.data.notfound2')]

    assert config.data.name == 'lorem'
    assert config.data.occupation == 'ipsum'
    assert config.data.Sound == 'latin'


def test_locations_python_first_multi_keys():

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    config = Config()
    config.locations = [
    Location.from_env_keys(['FOO', 'BAR', 'BAZ']),
    Location.from_env_python('TEST_SETTINGS_NOT_FOUND'),
    Location.from_python('tests.data.notfound2')
    ]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'


def test_locations_yaml_chain_multi():

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    os.environ['TEST_SETTINGS'] = 'tests.data.settings1'

    config = Config(chain=True)
    config.locations = [
    Location.from_env_keys(['FOO', 'BAR', 'BAZ']),
    Location.from_python('tests.data.settings2'),
    Location.from_env_python('TEST_SETTINGS'),
    ]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'

    assert config.data.CELERY_RESULT_BACKEND == 'amqp'

    assert config.data.CACHES['default']['BACKEND'] == \
    'django.core.cache.backends.memcached.MemcachedCache'

    assert 'south' in config.data.INSTALLED_APPS
    assert config.data.USE_TZ == True
    assert config.data.custom_show_toolbar() == True

    # testing extension
    assert config.data.EXTRA1 == 1
    assert config.data.EXTRA2 == 2

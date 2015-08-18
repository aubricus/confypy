import os
from confypy import Config
from confypy import Location


def test_config_init_json():
    config = Config()
    assert config is not None


def test_config_init_json_defaults():
    defaults = {'foo': 'bar'}
    config = Config(defaults=defaults)
    assert config.data.foo == 'bar'


def test_config_init_yaml():
    config = Config()
    assert config is not None


def test_config_init_yaml_defaults():
    defaults = {'foo': 'bar'}
    config = Config(defaults=defaults)
    assert config.data.foo == 'bar'


def test_config_defaults_get():
    defaults = {'foo': 'bar'}
    config = Config(defaults=defaults)
    assert config.data.get('foo', 22) == 'bar'
    assert config.data.get('bar', 22) == 22


def test_locations_env_keys():
    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    config = Config()
    config.locations = [Location.from_env_keys(['FOO', 'BAR', 'BAZ'])]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'

    assert config.data['FOO'] == '1'
    assert config.data['BAR'] == '2'
    assert config.data['BAZ'] == '3'


def test_locations_env_keys_chain():
    defaults = {'foo': 'bar'}

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    config = Config(defaults=defaults, chain=True)
    config.locations = [Location.from_env_keys(['FOO', 'BAR', 'BAZ'])]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'
    assert config.data.foo == 'bar'

    assert config.data['FOO'] == '1'
    assert config.data['BAR'] == '2'
    assert config.data['BAZ'] == '3'
    assert config.data['foo'] == 'bar'


def test_locations_env_keys_chain_replace():
    defaults = {'FOO': '20'}
    os.environ['FOO'] = '1'

    config = Config(defaults=defaults, chain=True)
    config.locations = [Location.from_env_keys(['FOO'])]

    assert config.data.FOO == '1'


def test_locations_env_keys_first_extend():
    defaults = {'FOO': '20'}
    os.environ['FOO'] = '1'

    config = Config(defaults=defaults)
    config.locations = [Location.from_env_keys(['FOO'])]

    config.extend({'BAR': 2})

    assert config.data.FOO == '1'
    assert config.data.BAR == 2


def test_locations_dict_first():

    config = Config()
    config.locations = [
    Location.from_dict({'name': 'Lucy'}),
    Location.from_dict({'name': 'Ollie'}),
    ]

    assert config.data.name == 'Lucy'


def test_locations_dict_chain():

    config = Config(chain=True)
    config.locations = [
    Location.from_dict({'name': 'Lucy'}),
    Location.from_dict({'nombre': 'Ollie'}),
    ]

    assert config.data.name == 'Lucy'
    assert config.data.nombre == 'Ollie'


def test_missing_env_key_with_defaults():
    defaults = {'ZAF': 'ducks'}

    config = Config(chain=True, defaults=defaults)
    config.locations = [
    Location.from_env_keys(['ZAF']),
    ]

    assert config.data.ZAF == 'ducks'


def test_missing_env_path():
    obj = Location.from_env_path('TEST_SETTINGS', parser='yaml')
    assert obj == {}

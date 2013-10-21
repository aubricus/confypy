import os
from confypy import Config
from confypy import Location


def test_locations_json_first():
    config = Config()
    config.locations = [Location.from_path('./tests/data/settings1.json')]

    assert config.data.name == 'Lucy'
    assert config.data.occupation == 'Dog'
    assert config.data.Sound == 'Woof'
    assert config.data['foo.bar.baz']['name'] == 'ollie'


def test_locations_json_first_env():
    os.environ['TEST_SETTINGS'] = './tests/data/settings1.json'

    config = Config()
    config.locations = [Location.from_env_path('TEST_SETTINGS')]

    assert config.data.name == 'Lucy'
    assert config.data.occupation == 'Dog'
    assert config.data.Sound == 'Woof'
    assert config.data['foo.bar.baz']['name'] == 'ollie'

    # attribute dict test
    assert config.data['foo.bar.baz'].name == 'ollie'
    assert config.data.extra3.foo.bar.baz == 'lucy'


def test_locations_json_first_multi():
    os.environ['TEST_SETTINGS'] = './tests/data/settings2.json'

    config = Config()
    config.locations = [
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/settings1.json')]

    assert config.data.name == 'Ollie'
    assert config.data.occupation == 'Cat'
    assert config.data.Sound == 'Meow'
    assert config.data['foo.bar.baz']['name'] == 'lucy'


def test_locations_json_first_multi_fail():
    os.environ['TEST_SETTINGS'] = './tests/data/notfound'

    config = Config()
    config.locations = [
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/settings1.json')]

    assert config.data.name == 'Lucy'
    assert config.data.occupation == 'Dog'
    assert config.data.Sound == 'Woof'
    assert config.data['foo.bar.baz']['name'] == 'ollie'


def test_locations_json_first_multi_defaults():
    os.environ['TEST_SETTINGS'] = './tests/data/notfound1'

    config = Config(defaults={
        'name': 'lorem',
        'occupation': 'ipsum',
        'Sound': 'latin'})

    config.locations = [
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/notfound2')]

    assert config.data.name == 'lorem'
    assert config.data.occupation == 'ipsum'
    assert config.data.Sound == 'latin'


def test_locations_json_first_multi_keys():

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    config = Config()
    config.locations = [
    Location.from_env_keys(['FOO', 'BAR', 'BAZ']),
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/notfound2')
    ]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'


def test_locations_json_chain_multi():

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    os.environ['TEST_SETTINGS'] = './tests/data/settings1.json'

    config = Config(chain=True)
    config.locations = [
    Location.from_env_keys(['FOO', 'BAR', 'BAZ']),
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/settings2.json')
    ]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'

    assert config.data.name == 'Ollie'
    assert config.data.occupation == 'Cat'
    assert config.data.Sound == 'Meow'
    assert config.data['foo.bar.baz']['name'] == 'lucy'

    # testing extension
    assert config.data.extra1 == 1
    assert config.data.extra2 == 1

    #testing attribute dict
    assert config.data.extra3.foo.bar.baz == 'lucy'

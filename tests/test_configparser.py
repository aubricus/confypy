import os
from confypy import Config
from confypy import Location


def test_locations_configparser_first():
    config = Config()
    config.locations = [Location.from_path('./tests/data/settings1.ini')]

    assert config.data.section1['foo'] == '1'
    assert config.data.section1['bar'] == '2'
    assert config.data.section1['baz'] == '3'

    assert config.data.section2['dog'] == 'lucy'
    assert config.data.section2['cat'] == 'ollie'


def test_locations_configparser_first_env():
    os.environ['TEST_SETTINGS'] = './tests/data/settings1.ini'

    config = Config()
    config.locations = [Location.from_env_path('TEST_SETTINGS')]

    assert config.data.section1['foo'] == '1'
    assert config.data.section1['bar'] == '2'
    assert config.data.section1['baz'] == '3'

    assert config.data.section2['dog'] == 'lucy'
    assert config.data.section2['cat'] == 'ollie'


def test_locations_configparser_first_multi():
    os.environ['TEST_SETTINGS'] = './tests/data/settings2.ini'

    config = Config()
    config.locations = [
        Location.from_env_path('TEST_SETTINGS'),
        Location.from_path('./tests/data/settings1.ini')
    ]

    assert config.data.section3['zap'] == '1'
    assert config.data.section3['qux'] == '2'
    assert config.data.section3['quux'] == '3'

    assert config.data.section4['lucy'] == 'dog'
    assert config.data.section4['ollie'] == 'cat'


def test_locations_configparser_first_multi_fail():
    os.environ['TEST_SETTINGS'] = './tests/data/notfound'

    config = Config()
    config.locations = [
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/settings1.ini')]

    assert config.data.section1['foo'] == '1'
    assert config.data.section1['bar'] == '2'
    assert config.data.section1['baz'] == '3'

    assert config.data.section2['dog'] == 'lucy'
    assert config.data.section2['cat'] == 'ollie'


def test_locations_configparser_first_multi_defaults():
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


def test_locations_configparser_first_multi_keys():

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


def test_locations_configparser_chain_multi():

    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    os.environ['TEST_SETTINGS'] = './tests/data/settings1.ini'

    config = Config(chain=True)
    config.locations = [
    Location.from_env_keys(['FOO', 'BAR', 'BAZ']),
    Location.from_env_path('TEST_SETTINGS'),
    Location.from_path('./tests/data/settings2.ini')
    ]

    assert config.data.FOO == '1'
    assert config.data.BAR == '2'
    assert config.data.BAZ == '3'

    assert config.data.section1['foo'] == '1'
    assert config.data.section1['bar'] == '2'
    assert config.data.section1['baz'] == '3'

    assert config.data.section2['dog'] == 'lucy'
    assert config.data.section2['cat'] == 'ollie'

    assert config.data.section3['zap'] == '1'
    assert config.data.section3['qux'] == '2'
    assert config.data.section3['quux'] == '3'

    assert config.data.section4['lucy'] == 'dog'
    assert config.data.section4['ollie'] == 'cat'

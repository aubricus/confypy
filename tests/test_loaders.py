import os
from confypy import loaders
from confypy.exceptions import LoadError


def test_load_file():
    data = loaders.load_file('./tests/data/settings1.json')
    assert len(data) > 0


def test_load_file_fail():
    try:
        loaders.load_file('./tests/data/settings9.json')
        assert False
    except LoadError:
        assert True


def test_load_env_path():
    os.environ['TEST_PATH'] = './tests/data/settings1.json'
    data = loaders.load_env_path('TEST_PATH')

    assert len(data) > 0


def test_load_env_path_fail():
    try:
        loaders.load_env_path('TEST_PATH_FAIL')
        assert False
    except LoadError:
        assert True


def test_load_env_keys():
    os.environ['FOO'] = '1'
    os.environ['BAR'] = '2'
    os.environ['BAZ'] = '3'

    data = loaders.load_env_keys(['FOO', 'BAR', 'BAZ'])

    assert data != {}
    assert data['FOO'] == '1'
    assert data['BAR'] == '2'
    assert data['BAZ'] == '3'


def test_load_env_keys_fail():

    data = loaders.load_env_keys(['QUX', 'ZAP', 'QUUX'])

    assert data != {}
    assert data['QUX'] == None
    assert data['ZAP'] == None
    assert data['QUUX'] == None

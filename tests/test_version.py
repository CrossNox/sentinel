from sentinel import __version__


def test_import_version():
    assert __version__ >= "0.1.0"

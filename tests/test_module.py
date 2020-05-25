import toml

import samplespace
import docs.source.conf

PROJECT_FILE = '../pyproject.toml'


def test_version():
    with open(PROJECT_FILE, 'r') as f:
        config = toml.load(f)

    version = config['tool']['poetry']['version']
    assert samplespace.__version__ == version
    assert docs.source.conf.release == version

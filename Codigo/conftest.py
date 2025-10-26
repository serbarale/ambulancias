import pytest
import sys, os

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(autouse=True)
def setup_test_environment(settings):
    settings.ROOT_URLCONF = 'urlconf'
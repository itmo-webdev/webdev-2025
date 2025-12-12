import random
import pytest

@pytest.fixture(scope="session")
def sess():
    return random.randint(0, 100)

@pytest.fixture
def func():
    return random.randint(0, 100)

def test1(sess, func):
    raise

def test2(sess, func):
    raise


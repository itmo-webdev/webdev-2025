import pytest

@pytest.fixture(scope="session")
def order():
    return []

@pytest.fixture
def func(order):
    order.append("func")

@pytest.fixture(scope="class")
def cls(order):
    order.append("class")

@pytest.fixture(scope="module")
def mod(order):
    order.append("module")

@pytest.fixture(scope="package")
def pkg(order):
    order.append("package")

@pytest.fixture(scope="session")
def sess(order):
    order.append("session")

class TestClass:
    def test_order(self, func, cls, mod, pkg, sess, order):
        assert order == ["session", "package", "module", "class", "func"]


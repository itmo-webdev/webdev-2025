import pytest

def sum_arif(l: list[int]) -> int:
    if len(l) == 0:
        return 0
    return (l[0] + l[-1]) * len(l) // 2

@pytest.fixture
def mylist_10():
    return [i for i in range(10)]

def test_sum_arif(mylist_10):
    print("capture stdout")
    assert sum_arif(mylist_10) == sum(mylist_10)

@pytest.mark.parametrize("l", [
    [i for i in range(N)]
    for N in range(4, 100)
])
def test_sum_arif_parametrized(l):
    assert sum_arif(l) == sum(l)

@pytest.mark.parametrize("l", [
    *[[i for i in range(N)] for N in range(4, 50)]
    + [[10, 0, 5, 2]]
    + [[i for i in range(N)] for N in range(50, 100)]
])
def test_error(l):
    assert sum_arif(l) == sum(l)



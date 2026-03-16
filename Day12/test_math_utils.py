from math_utils import add
from math_utils import div
import pytest

def test_add():
    assert add(2,3) == 5

def test_add_negative():
    assert add(-2,-3) == -5

def test_add_zero():
    assert add(5,0) == 5

def test_divide():
    assert div(10,5) == 2

def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        div(5,0)

@pytest.mark.parametrize(
    "a,b,ans",[
        (2,5,7),
        (-2,-3,-5),
        (5,0,5)
    ]
)

def test_all_add(a,b,ans):
    assert add(a,b) == ans
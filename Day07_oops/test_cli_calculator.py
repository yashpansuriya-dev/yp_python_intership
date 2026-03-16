import cli_calculator
import pytest
from cli_calculator import add
from cli_calculator import sub
from cli_calculator import multi
from cli_calculator import div
from cli_calculator import power
from cli_calculator import rem
from cli_calculator import sqrt

# -------------------------------------------------------------------

def test_add():
    assert add(2,3) == 5


def test_sub():
    assert sub(5,3) == 2


def test_multi():
    assert multi(5,3) == 15


def test_multi_large():
    assert multi(8,1000000) == 8000000


def test_div():
    assert div(10,2) == 5


def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        div(3,0)


def test_power():
    assert power(5,3) == 125


def test_power_large():
    num = 7888609052210118054117285652827862296732064351090230047702789306640625
    assert power(5,100) == num


def test_rem():
    assert rem(10,4) == 2


def test_sqrt():
    assert sqrt(25) == 5.0

# -------------------------------------------------------------------

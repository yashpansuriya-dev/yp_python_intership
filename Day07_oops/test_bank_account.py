from bank_account import BankAccount
from bank_account import SavingAccount
import pytest

# Reusable test setup
@pytest.fixture
def acc():
    return BankAccount("yash", 1000, 1234)

@pytest.fixture
def sav():
    return SavingAccount("yash", 1000, 1234)

def test_initial_balance(acc):
    assert acc.get_balance() == 1000

def test_deposit(acc):
    acc.deposit(2000)

    assert acc.get_balance() == 3000

def test_withdraw(acc):
    acc.withdraw(500)

    assert acc.get_balance() == 500

def test_withdraw_insufficient_balance(acc):
    acc.withdraw(1500)

    assert acc.get_balance() == 1000

def test_negative_deposit(acc):
    acc.deposit(-200)

    assert acc.get_balance() == 1000


def test_monthly_interest(sav):
    sav.monthly_interest(10)

    assert sav.get_balance() == 1100

def test_monthly_interest_negative(sav):
    sav.monthly_interest(-10)

    assert sav.get_balance() == 1000    

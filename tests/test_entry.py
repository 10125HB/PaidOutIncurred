import pytest

from pydantic import ValidationError

from paidoutsincurred.entry import Entry


def test_paid():
    entry = Entry(paid=100)

    assert entry.paid == 100
    assert entry.outstanding is None
    assert entry.incurred is None


def test_outstanding():
    entry = Entry(outstanding=100)

    assert entry.paid is None
    assert entry.outstanding == 100
    assert entry.incurred is None


def test_incurred():
    entry = Entry(incurred=100)

    assert entry.paid is None
    assert entry.outstanding is None
    assert entry.incurred == 100


def test_paid_and_outstanding():
    entry = Entry(paid=100, outstanding=50)

    assert entry.paid == 100
    assert entry.outstanding == 50
    assert entry.incurred == 150


def test_paid_and_incurred():
    entry = Entry(paid=100, incurred=150)

    assert entry.paid == 100
    assert entry.outstanding == 50
    assert entry.incurred == 150


def test_outstanding_and_incurred():
    entry = Entry(outstanding=50, incurred=150)

    assert entry.paid == 100
    assert entry.outstanding == 50
    assert entry.incurred == 150


def test_all_set_ok():
    entry = Entry(paid=100, outstanding=50, incurred=150)

    assert entry.paid == 100
    assert entry.outstanding == 50
    assert entry.incurred == 150


def test_all_set_inconsistent():
    with pytest.raises(ValidationError):
        Entry(paid=50, outstanding=100, incurred=200)

"""Multiplier test cases"""
from proj.helpers import multiplier

def test_mulitplier_easy():
    """Test multiplier (easy)"""
    a=3
    b=4
    expected=a*b
    actual=multiplier(a,b)
    assert actual==expected

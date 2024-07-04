"""Multiplier test cases"""
from ..libreed.helpers import banner

def test_banner():
    """Test banner"""
    expected="## Hello ##"
    actual=banner("Hello", 11)
    assert actual==expected

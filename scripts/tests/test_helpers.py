"""Helper test cases"""
from libreed.helpers import banner,text_to_n_rows

def test_banner():
    """Test banner"""
    expected="## Hello ##"
    actual=banner("Hello", 11)
    assert actual==expected

def test_text_to_n_rows_trunc():
    """Test text_to_n_rows when input is truncated"""
    lines = [f"row {i}" for i in range(10)]
    num_rows = 3
    full_text = "\n".join(lines)
    expected = "\n".join([f"row {i}" for i in range(7,10)])
    actual = text_to_n_rows(text=full_text, num_rows=num_rows, blank_line_filler='#')
    assert expected == actual

def test_text_to_n_rows_fill():
    """Test text_to_n_rows when input is filled"""
    lines = [f"row {i}" for i in range(2)]
    num_rows = 4
    full_text = "\n".join(lines)
    expected = "\n".join([f"row {i}" for i in range(2)] + ['#', '#'])
    actual = text_to_n_rows(text=full_text, num_rows=num_rows, blank_line_filler='#')
    assert expected == actual
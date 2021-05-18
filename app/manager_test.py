# import some code we want to test

from app.manager import to_Percentage, from_CSV, stock_entry

def test_to_Percentage():
    assert to_Percentage(0.24678) == "24.68%"

     #edge cases 
    assert to_Percentage(.9999999999999) == "100.0%"
    assert to_Percentage(0.0000023) == "0.0%"

def test_from_CSV():
    validResults = from_CSV('test/MockData/mock_stock_data.csv')

    assert validResults == ['AAPL', 'FB', 'MSFT', 'NFLX', 'PYPL']

class WeightFactory(object):

    def __init__(self, ticker_list, stock_db, required_return):
        """Initialize the weight.

        Args:
            ticker_list {list}: List of ticker symbols to weight.
            stock_db {StockDatabase}: Database of necessary stock data.
            required_return {float}: Return required to pay bills.
        """
        self._ticker_list = ticker_list
        self._stock_db = stock_db
        self._required_return = required_return

    def Solve(self):
        """Actually solve the factory."""
        pass

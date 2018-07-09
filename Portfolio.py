import numpy as np


class Portfolio(object):
    """Stores information about a current, desired, or potential portfolio."""

    def __init__(self, percent_allocations, stock_db):
        """Initialize the portfolio.

        Args:
            percent_allocations {dict}: Dictionary of tickers to percent
                allocations.
            stock_db {StockDatabase}: Database of necessary information.
        """
        self._stock_db = stock_db
        self.percent_allocations = percent_allocations
        self.backtested_returns = self._getBacktestedReturns()

    def _getBacktestedReturns(self):
        """Calculate backtested returns for the portfolio.

        Returns:
            backtested_returns {OrderedDict}: Dictionary of dates to returns,
                with dates in order.
        """
        # Get allocations in same order as stock database.
        allocation_array = []
        for ticker in self._stock_db.tickers:
            if ticker in self.percent_allocations:
                allocation_array.append([self.percent_allocations[ticker]])
            else:
                allocation_array.append([0])
        allocation_array = np.array(allocation_array, dtype=np.float64)

        nested_returns = np.matmul(
            self._stock_db.price_change_array, allocation_array)
        return np.transpose(nested_returns)[0]

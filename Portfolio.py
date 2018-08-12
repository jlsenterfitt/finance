import numpy as np
from scipy.stats.mstats import gmean


class Portfolio(object):
    """Stores information about a current, desired, or potential portfolio."""

    def __init__(
            self,
            stock_db,
            percent_allocations=[],
            percent_allocations_dict={}):
        """Initialize the portfolio.

        Args:
            stock_db {StockDatabase}: Database of necessary information.
            percent_allocations {list}: List of percent allocations.
            percent_allocations_dict {dict}: Dictionary of tickers to percent
                allocations.
        """
        self._stock_db = stock_db
        self.allocation_array = self._getPercentAllocations(
            percent_allocations, percent_allocations_dict)
        self.backtested_returns = self._getBacktestedReturns()
        self.average_return = gmean(self.backtested_returns)
        # TODO: Add portfolio stdev (testing only).
        # TODO: Add downside risk (s).
        # TODO: Add downside correlation.
        # TODO: Add score.

    def _getPercentAllocations(
            self, percent_allocations, percent_allocations_dict):
        """Convert a list or dict of allocations to a list of allocations.

        Args:
            percent_allocations {list}: List of percent allocations.
            percent_allocations_dict {dict}: Dictionary of tickers to percent
                allocations.
        Returns:
            percent_allocations {array}: Array of percent allocations.
        """
        # Get allocations in same order as stock database.
        if percent_allocations_dict:
            allocation_array = []
            for ticker in self._stock_db.tickers:
                if ticker in percent_allocations_dict:
                    allocation_array.append(
                        [percent_allocations_dict[ticker]])
                else:
                    allocation_array.append([0])
            allocation_array = np.array(allocation_array, dtype=np.float64)
        else:
            allocation_array = np.array(percent_allocations, dtype=np.float64)
        return allocation_array

    def _getBacktestedReturns(self):
        """Calculate backtested returns for the portfolio.

        Returns:
            backtested_returns {OrderedDict}: Dictionary of dates to returns,
                with dates in order.
        """
        nested_returns = np.matmul(
            self._stock_db.price_change_array, self.allocation_array)
        return np.transpose(nested_returns)[0]

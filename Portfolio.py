import numpy as np
from scipy.stats.mstats import gmean

import Config


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

        self.downside_risk = None
        self.downside_correl = None
        self.score = None

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
        allocation_array = []
        if percent_allocations_dict:
            for ticker in self._stock_db.tickers:
                if ticker in percent_allocations_dict:
                    allocation_array.append(
                        percent_allocations_dict[ticker])
                else:
                    allocation_array.append(0)
            allocation_array = np.array(allocation_array, dtype=np.float64)
        else:
            allocation_array = np.array(percent_allocations, dtype=np.float64)
        return allocation_array

    def _getBacktestedReturns(self):
        """Calculate backtested returns for the portfolio.

        Returns:
            backtested_returns {Array}: Dictionary of dates to returns,
                with dates in order.
        """
        return np.matmul(
            self._stock_db.price_change_array, self.allocation_array)

    def getScore(self, required_return):
        """Calculate the score of this portfolio using a modifed Sortino Ratio.

        Score = (avg_return - wanted_return) / \
                 (downside_risk * downside_correl)
        avg_return = geometric mean of backdated returns.
        wanted_return = internal rate of return for long term budget.
        downside_risk = downside semivariance of portfolio below wanted return.
        downside_correl = correl of portfolio in periods below wanted return.

        Args:
            required_return {float}: The required level of return per year.
        Returns:
            score {float}: The modified Sortino Ratio of this portfolio.
        """
        # De-annualize the required return.
        required_return = np.power(required_return, 1.0 / Config.DAYS_IN_YEAR)

        # Short-circuit evaluation if the given portfolio is below the desired amount.
        """
        if self.average_return < required_return:
            self.score = self.average_return - required_return
            return self.score
        """

        # Determine downside_risk.
        returns = np.copy(self.backtested_returns)
        returns -= required_return
        returns = np.clip(returns, None, 0)
        returns *= returns
        downside_risk = np.sqrt(np.sum(returns) / returns.size)
        self.downside_risk = downside_risk

        # Determine downside_correl.
        returns = np.copy(self.backtested_returns)
        below_desired = returns < required_return
        filtered_returns = [
            self._stock_db.price_change_array[x]
            for x in xrange(len(below_desired)) if below_desired[x]]
        downside_correl = np.matmul(
            np.matmul(
                self.allocation_array,
                np.corrcoef(filtered_returns, rowvar=False)),
            self.allocation_array)
        self.downside_correl = downside_correl

        # Determine score.
        score = (
            (self.average_return - required_return)
            / (downside_risk * downside_correl))
        self.score = score
        return score

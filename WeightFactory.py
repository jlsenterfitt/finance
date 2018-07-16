import numpy as np


def GetBackdatedReturns(weights, return_matrix):
    """Get an array of backdated returns based on input weights.

    Args:
        weights {array}: A list of weights.
        return_matrix {matrix}: The matrix of all historical returns.
    Returns:
        backdated_returns {array}: An array of backdated portfolio returns.
    """
    return np.matmul(weights, return_matrix)


def EstimateDistributionParameters():
    pass


def CalcDownsideRisk():
    pass


def CalcModifiedSortinoRatio():
    pass


def CalcScore(weights, *args):
    """Generate the score of a given set of weights.

    Goal is to minimize a modified Sortino Ratio (below), defined as the
        portfolio's return divided by it's cumulative downside risk. This
        differs in that no single required return is defined (since each
        year has its own), and the downside risk is the sum of all downside
        risks for the future.
    https://en.wikipedia.org/wiki/Sortino_ratio

    Args:
        weights {array}: An array of weights.
        *args {tuple}: A set of constants for calculating the score.
            arg0 {list}: A list of required IRRs.
            arg1 {matrix}: Matrix of price changes over time.
    Returns:
        score {float}: The modified Sortino Ratio of this set of weights.
    """
    # First, create an array of backdated prices for the given weights.

    # Second, estimate the parameters for the lognormal distribution of price
    # changes for this portfolio.

    # Third, loop over required IRRs and determine downside risk for each.
    # https://docs.scipy.org/doc/scipy/reference/tutorial/integrate.html

    # Fourth, calculate the modified Sortino Ratio.

    # TODO-implement
    pass


class WeightFactory(object):
    """Generates desired weights."""

    def __init__(self, stock_db, required_return):
        """Initialize the weight factory.

        Args:
            stock_db {StockDatabase}: Database of necessary stock data.
            required_return {float}: Return required to pay bills.
        """
        self._stock_db = stock_db
        self._required_return = required_return
        self.desored_alloc_dict = None

    def Solve(self):
        """Actually run the solver.

        Several optimization methods are given vai SciPy (below). Will need to
            test them to find a simple, efficient, and robust version.
        https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#constrained-minimization-of-multivariate-scalar-functions-minimize

        Mystic (below) could also be useful.
        http://mystic.readthedocs.io/en/latest/index.html

        Returns:
            desired_allocations {dict}: Dictionary of tickers to percent
                allocations.
        """
        # TODO-implement
        pass

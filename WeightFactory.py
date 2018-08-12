import numpy as np


def CalcScore(weights, *args):
    """Generate the score of a given set of weights.

    Goal is to minimize a modified Sortino Ratio (below), defined as the
        portfolio's excess return divided by it's cumulative downside risk and
        its internal downside correlation. The internal downside correlation
        is the correlation of the portfolio in each underperforming period.
    https://en.wikipedia.org/wiki/Sortino_ratio

    Args:
        weights {array}: An array of weights.
        *args {tuple}: A set of constants for calculating the score.
            arg0 {float}: The required IRR.
            arg1 {matrix}: Matrix of price changes over time.
    Returns:
        score {float}: The modified Sortino Ratio of this set of weights.
    """
    # First, create an array of backdated prices for the given weights.
    # (r_id)

    # Second, get the backdated return of the portfolio.
    # (R-bar)

    # Third, calculate the downside risk for the portolio.
    # (s)

    # Fourth, calculate the downside correlation for the portfolio.
    # (c)

    # Finally, calculate the modified Sortino Ratio.
    # (m)

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

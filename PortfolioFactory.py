import numpy as np


class PortfolioFactory(object):
    """Generates desired portfolio."""

    def __init__(self, stock_db, required_return):
        """Initialize the weight factory.

        Args:
            stock_db {StockDatabase}: Database of necessary stock data.
            required_return {float}: Return required to pay bills.
        """
        self._stock_db = stock_db
        self._required_return = required_return

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

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

    def _calcScore(self):
        """Generate the score of a given set of weights.

        Goal is to minimize a modified Sortino Ratio (below), defined as the
            portfolio's return divided by it's cumulative downside risk. This
            differs in that no single required return is defined (since each
            year has its own), and the downside risk is the sum of all downside
            risks for the future.
        https://en.wikipedia.org/wiki/Sortino_ratio

        Args:
            weights {list}: A list of weights.
        Returns:
            score {number}: The modified Sortino Ratio of this set of weights.
        """
        # TODO-implement
        pass

import numpy as np

from Portfolio import Portfolio


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
        self.desired_portfolio = self._Solve()

    def _Solve(self):
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
        # Finish from here https://script.google.com/macros/d/M2sMb_Qv7K4-zRk8zO2S6qReMw4PaOM-o/edit?uiv=2&mid=ACjPJvGbqWeOEuR7sqFILpOQ0A1K_4KOZw83rOPs90VgW2xlmO8DV1MkDJIknocG0rNTor0Hj2meHRO66vMBIeN_ZNSbK17O9IOQY-IDUF3ASouro_UGfrxfGDic3eB6nHOGuUVM6Cguidw
        # Start with the first stock arbitrarily at 100%.
        allocations = np.zeros(len(self._stock_db.tickers))
        allocations[0] = 1

        portfolio = Portfolio(self._stock_db, percent_allocations=allocations)
        score = portfolio.getScore(self._required_return)

        return portfolio

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

        Uses a binary heuristic to optimize the solution. Start with 100% in an
            arbitrary fund, then try to trade all 100% into another fund.
            Continue until no 100% trade gives a benefit. Then attempt 50% with
            the same logic, and continue until an insignificant amount is being
            traded.

        Theorhetically this could fall prey to local maxima, so improvements
            should be sought.
        TODO: Attempt Simulated Annealing.

        Returns:
            desired_allocations {dict}: Dictionary of tickers to percent
                allocations.
        """
        minorSteps = 0
        majorSteps = 0
        best = np.zeros(len(self._stock_db.tickers))
        best[0] = 1
        portfolio = Portfolio(self._stock_db, percent_allocations=best)
        bestScore = portfolio.getScore(self._required_return)

        tradeAmount = 1
        while tradeAmount >= 0.00001:
            improved = False

            for sell in xrange(len(best)):
                if best[sell] < tradeAmount:
                    continue

                for buy in xrange(len(best)):
                    if buy == sell:
                        continue

                    curr = np.copy(best)
                    curr[sell] -= tradeAmount
                    curr[buy] += tradeAmount

                    portfolio = Portfolio(
                        self._stock_db, percent_allocations=curr)
                    currScore = portfolio.getScore(self._required_return)

                    minorSteps += 1
                    if currScore > bestScore:
                        bestScore = currScore
                        best = np.copy(curr)
                        improved = True
                        majorSteps += 1

            if not improved:
                tradeAmount /= 2.0

        portfolio = Portfolio(self._stock_db, percent_allocations=best)
        portfolio.getScore(self._required_return)

        print ('Major steps %d' % majorSteps)
        print ('Minor steps %d' % minorSteps)
        return portfolio

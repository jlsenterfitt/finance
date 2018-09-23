import math
from multiprocessing.dummy import Pool
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
        self.desired_portfolio = self._BinarySolve()

    def _BinarySolveIndividualSell(self, input_args):
        """Check if an individual sale of stock is an improvement on the current regime."""
        (best, trade_amount, best_score, sell) = input_args
        if best[sell] < trade_amount:
            return (best, best_score)

        curr = np.copy(best)

        for buy in xrange(len(best)):
            if buy == sell:
                continue

            curr[sell] -= trade_amount
            curr[buy] += trade_amount

            portfolio = Portfolio(self._stock_db, percent_allocations=curr)
            curr_score = portfolio.getScore(self._required_return)

            if curr_score > best_score:
                best_score = curr_score
                best = np.copy(curr)

            curr[sell] += trade_amount
            curr[buy] -= trade_amount

        return (best, best_score)

    def _BinarySolve(self):
        """Actually run the solver.

        Uses a binary heuristic to optimize the solution. Start with 100% in an
            arbitrary fund, then try to trade all 100% into another fund.
            Continue until no 100% trade gives a benefit. Then attempt 50% with
            the same logic, and continue until an insignificant amount is being
            traded.

        Theoretically this could fall prey to local maxima, so improvements
            should be sought.
        TODO: Attempt Simulated Annealing w/ ~32k portfolios.
        TODO: Attempt Genetic Algorithm w/ ~32k portfolios.

        Returns:
            desired_allocations {dict}: Dictionary of tickers to percent
                allocations.
        """
        major_steps = 0
        best = np.zeros(len(self._stock_db.tickers))
        best[0] = 1
        portfolio = Portfolio(self._stock_db, percent_allocations=best)
        best_score = portfolio.getScore(self._required_return)
        pool = Pool()

        trade_amount = 1
        # Run until rounding is +/- 1 basis point.
        while trade_amount >= 0.00005:
            improved = False

            inputs = []
            for sell in xrange(len(best)):
                inputs.append((np.copy(best), trade_amount, best_score, sell))

            results = pool.map(self._BinarySolveIndividualSell, inputs, int(
                math.ceil(math.sqrt(len(inputs)))))

            for result in results:
                (curr, curr_score) = result
                if curr_score > best_score:
                    best_score = curr_score
                    best = np.copy(curr)
                    improved = True
                    major_steps += 1

            if not improved:
                trade_amount /= 2.0
                print('New trade amount: %f' % trade_amount)
            else:
                print('Improvements: %d, score: %f' %
                      (major_steps, best_score))

        portfolio = Portfolio(self._stock_db, percent_allocations=best)
        portfolio.getScore(self._required_return)

        print ('Major steps %d' % major_steps)
        return portfolio

import math
import numpy as np
import random
import time

from Portfolio import Portfolio


class PortfolioFactory(object):
    """Generates desired portfolio."""

    def __init__(self, stock_db, required_return, use_genetic=False):
        """Initialize the weight factory.

        Args:
            stock_db {StockDatabase}: Database of necessary stock data.
            required_return {float}: Return required to pay bills.
        """
        self._stock_db = stock_db
        self._required_return = required_return
        init_allocation = None
        if use_genetic:
            init_allocation = self._GeneticSolve().allocation_array
        self.desired_portfolio = self._BinarySolve(
            init_allocation=init_allocation)

    def _GeneticSolve(self):
        """Attempt to find an optimal solution via a genetic algorithm."""
        print('Starting Genetic Algo...')
        generation_size = len(self._stock_db.tickers)
        best_to_keep = int(math.ceil(math.sqrt(generation_size)))
        max_portfolios = generation_size * generation_size
        num_portfolios = 0
        generation = 0
        mutation_rate = 0.05
        min_time = 60
        start = time.time()

        # Generate initial random candidates.
        population = []
        for i in range(generation_size):
            allocations = np.random.randint(2, size=generation_size)
            allocations = allocations / (allocations.sum() + 0.0)
            portfolio = Portfolio(
                self._stock_db, percent_allocations=allocations)
            portfolio.getScore(self._required_return)
            population.append(portfolio)
            num_portfolios += 1

        # Generate some non-random candidates.
        for i in range(generation_size):
            allocations = np.zeros(generation_size)
            allocations[i] = 1.0
            portfolio = Portfolio(
                self._stock_db, percent_allocations=allocations)
            portfolio.getScore(self._required_return)
            population.append(portfolio)
            num_portfolios += 1
        population.sort(key=lambda p: p.score, reverse=True)

        # 5) Repeat 2-5 until X portfolios have been tried.
        while (num_portfolios < max_portfolios or (time.time() - start) < min_time):
            print('Generation %d best is %f' %
                  (generation, population[0].score))
            generation += 1
            # 2) Keeping top X%, cull randomly to under Y%.
            while len(population) > best_to_keep * 2:
                del population[random.randint(
                    best_to_keep, len(population) - 1)]

            # 3) Choose parents (based randomly on score) and breed.
            while len(population) < generation_size:
                parent_1 = random.choice(population)
                parent_2 = random.choice(population)
                while parent_1 == parent_2:
                    parent_2 = random.choice(population)

                # 3) Merging genes is 50/50 odds of getting each parents allocation for a stock.
                allocations = np.zeros(len(self._stock_db.tickers))
                for allocation_index in range(len(allocations)):
                    if random.random() < mutation_rate:
                        allocations[allocation_index] = random.random()
                    elif random.random() < 0.5:
                        allocations[allocation_index] = parent_1.allocation_array[allocation_index]
                    else:
                        allocations[allocation_index] = parent_2.allocation_array[allocation_index]

                # Especially in the beginning, all zeroes is possible.
                if allocations.sum() == 0:
                    continue

                # Normalize.
                allocations = allocations / (allocations.sum() + 0.0)
                portfolio = Portfolio(
                    self._stock_db, percent_allocations=allocations)
                portfolio.getScore(self._required_return)
                population.append(portfolio)
                num_portfolios += 1

            population.sort(key=lambda p: p.score, reverse=True)

        return population[0]

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

    def _BinarySolve(self, init_allocation=None):
        """Actually run the solver.

        Uses a binary heuristic to optimize the solution. Start with 100% in an
            arbitrary fund, then try to trade all 100% into another fund.
            Continue until no 100% trade gives a benefit. Then attempt 50% with
            the same logic, and continue until an insignificant amount is being
            traded.

        Theoretically this could fall prey to local maxima, so improvements
            should be sought.
        TODO: Attempt Simulated Annealing w/ ~32k portfolios.
        TODO: Attempt a middle ground of genetic and binary.
            # Create a basic portfolio w/ genetic, then run through binary to finesse it.
            # Add a caveat that trade_amount = min(trade_amount, best[sell])

        Returns:
            desired_allocations {dict}: Dictionary of tickers to percent
                allocations.
        """
        print('Starting Binary Algo...')
        major_steps = 0
        if init_allocation is None:
            init_allocation = np.zeros(len(self._stock_db.tickers))
            init_allocation[0] = 1
        best = init_allocation
        portfolio = Portfolio(self._stock_db, percent_allocations=best)
        best_score = portfolio.getScore(self._required_return)
        # When rounded, translates to +/- 1 basis point.
        min_trade_amount = 0.00005
        max_time = 3600

        trade_amount = 1
        full_start = time.time()
        while trade_amount >= min_trade_amount and time.time() - full_start < max_time:
            improved = False

            inputs = []
            for sell in xrange(len(best)):
                if best[sell] < trade_amount:
                    continue
                inputs.append((np.copy(best), trade_amount, best_score, sell))

            start = time.time()
            results = map(self._BinarySolveIndividualSell, inputs)
            print('Selling %d took %d seconds' % (len(inputs), time.time() - start))

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

from collections import OrderedDict
from decimal import Decimal
import numpy as np
import unittest

import Config
from Stock import Stock
from StockDatabase import StockDatabase
from Portfolio import Portfolio


class Test_Portfolio(unittest.TestCase):

    def setUp(self):
        # Change the config value.
        Config.MINIMUM_AMOUNT_DATA = 4
        Config.DAYS_IN_YEAR = 1

        test_data = OrderedDict()
        test_data['2018-01-01'] = Decimal('100.00')
        test_data['2018-01-02'] = Decimal('102.00')
        test_data['2018-01-03'] = Decimal('104.00')
        test_data['2018-01-04'] = Decimal('108.00')
        test_data['2018-01-05'] = Decimal('110.00')
        stock1 = Stock(test_data, '1', 0)

        test_data = OrderedDict()
        test_data['2018-01-01'] = Decimal('200.00')
        test_data['2018-01-02'] = Decimal('202.00')
        test_data['2018-01-03'] = Decimal('206.00')
        test_data['2018-01-04'] = Decimal('208.00')
        test_data['2018-01-05'] = Decimal('210.00')
        stock2 = Stock(test_data, '2', 0)

        test_data = OrderedDict()
        test_data['2018-01-01'] = Decimal('300.00')
        test_data['2018-01-02'] = Decimal('309.00')
        test_data['2018-01-03'] = Decimal('318.00')
        test_data['2018-01-04'] = Decimal('327.00')
        test_data['2018-01-05'] = Decimal('336.00')
        stock3 = Stock(test_data, '3', 0)

        test_stock_dict = {'1': stock1, '2': stock2, '3': stock3}

        self.stock_db = StockDatabase(test_stock_dict)

    def test_getPercentAllocationsDict(self):
        percent_allocations = {'1': 0.5, '2': 0.4, '3': 0.1}
        portfolio = Portfolio(
            self.stock_db, percent_allocations_dict=percent_allocations)
        self.assertListEqual(list(portfolio.allocation_array), [0.5, 0.4, 0.1])

    def test_getPercentAllocationsArray(self):
        percent_allocations = [0.5, 0.4, 0.1]
        portfolio = Portfolio(
            self.stock_db, percent_allocations=percent_allocations)
        self.assertListEqual(list(portfolio.allocation_array), [0.5, 0.4, 0.1])

    def test_getBacktestedReturns(self):
        percent_allocations = {'1': 0.5, '2': 0.4, '3': 0.1}
        portfolio = Portfolio(
            self.stock_db, percent_allocations_dict=percent_allocations)
        self.assertAlmostEqual(list(portfolio.backtested_returns)[0], 1.017)
        self.assertEqual(len(portfolio.backtested_returns), 4)

    def test_averageReturn(self):
        percent_allocations = {'1': 0.5, '2': 0.4, '3': 0.1}
        portfolio = Portfolio(
            self.stock_db, percent_allocations_dict=percent_allocations)
        self.assertAlmostEqual(portfolio.average_return, 1.0198523)

    def test_downsideRisk(self):
        portfolio = Portfolio(
            self.stock_db, percent_allocations=[0.5, 0.4, 0.1])
        returns = np.array([1.01, 1.02, 1.03, 1.04, 1.05], dtype=np.float64)
        portfolio.backtested_returns = returns
        portfolio._stock_db.price_change_array = [
            [1.00, 1.01, 1.02],
            [1.01, 1.02, 1.03],
            [1.02, 1.03, 1.04],
            [1.03, 1.04, 1.05],
            [1.04, 1.05, 1.06]
        ]
        portfolio.getScore(1.03)
        self.assertAlmostEqual(portfolio.downside_risk, 0.01)

    def test_downsideCorrel(self):
        portfolio = Portfolio(
            self.stock_db, percent_allocations=[0.5, 0.4, 0.1])
        returns = np.array([1.01, 1.02, 1.03, 1.04, 1.05], dtype=np.float64)
        portfolio.backtested_returns = returns
        portfolio._stock_db.price_change_array = [
            [1.00, 1.01, 1.02],
            [1.01, 1.00, 1.03],
            [1.02, 0.99, 1.04],
            [1.03, 0.98, 1.05],
            [1.04, 0.97, 1.06]
        ]
        portfolio.getScore(1.05)
        self.assertAlmostEqual(portfolio.downside_correl, 0.04)

    def test_score(self):
        portfolio = Portfolio(
            self.stock_db, percent_allocations=[0.5, 0.4, 0.1])
        returns = np.array([1.01, 1.02, 1.03, 1.04, 1.05], dtype=np.float64)
        portfolio.backtested_returns = returns
        portfolio._stock_db.price_change_array = [
            [1.00, 1.01, 1.02],
            [1.01, 1.00, 1.03],
            [1.02, 0.99, 1.04],
            [1.03, 0.98, 1.05],
            [1.04, 0.97, 1.06]
        ]
        score = portfolio.getScore(1.021)
        self.assertAlmostEqual(portfolio.score, -5.80858974126046)
        self.assertAlmostEqual(score, -5.80858974126046)


if __name__ == '__main__':
    unittest.main()

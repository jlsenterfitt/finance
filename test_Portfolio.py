from collections import OrderedDict
from decimal import Decimal
import unittest

import Config
from Stock import Stock
from StockDatabase import StockDatabase
from Portfolio import Portfolio


class Test_Portfolio(unittest.TestCase):

    def setUp(self):
        # Change the config value.
        Config.MINIMUM_AMOUNT_DATA = 4

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

    def test_getBacktestedReturns(self):
        percent_allocations = {'1': 0.5, '2': 0.4, '3': 0.1}
        portfolio = Portfolio(
            self.stock_db, percent_allocations_dict=percent_allocations)
        self.assertAlmostEqual(list(portfolio.backtested_returns)[0], 1.017)
        self.assertEqual(len(portfolio.backtested_returns), 4)


if __name__ == '__main__':
    unittest.main()

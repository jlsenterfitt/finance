from collections import OrderedDict
from decimal import Decimal
import unittest

import Config
from Stock import Stock
from StockDatabase import StockDatabase
from Portfolio import Portfolio
from PortfolioFactory import PortfolioFactory


class Test_Portfolio(unittest.TestCase):

    def setUp(self):
        # Change the config value.
        Config.MINIMUM_AMOUNT_DATA = 4

        test_data = OrderedDict()
        test_data['2018-01-09'] = Decimal('145.69')
        test_data['2018-01-08'] = Decimal('146.25')
        test_data['2018-01-07'] = Decimal('147.17')
        test_data['2018-01-06'] = Decimal('147.27')
        test_data['2018-01-05'] = Decimal('147.41')
        test_data['2018-01-04'] = Decimal('146.93')
        test_data['2018-01-03'] = Decimal('146.27')
        test_data['2018-01-02'] = Decimal('145.78')
        test_data['2018-01-01'] = Decimal('144.92')
        stock1 = Stock(test_data, '1', 0)

        test_data = OrderedDict()
        test_data['2018-01-09'] = Decimal('79.19')
        test_data['2018-01-08'] = Decimal('79.18')
        test_data['2018-01-07'] = Decimal('79.02')
        test_data['2018-01-06'] = Decimal('78.87')
        test_data['2018-01-05'] = Decimal('78.89')
        test_data['2018-01-04'] = Decimal('79.03')
        test_data['2018-01-03'] = Decimal('78.96')
        test_data['2018-01-02'] = Decimal('78.79')
        test_data['2018-01-01'] = Decimal('78.75')
        stock2 = Stock(test_data, '2', 0)

        test_stock_dict = {'1': stock1, '2': stock2}

        self.stock_db = StockDatabase(test_stock_dict)

    def test_default(self):
        # Here be dragons: This serves as a pseudo integration test for
        # StockDB, Portfolio, and PortfolioFactory.
        pf = PortfolioFactory(self.stock_db, 1.0)
        # Only run to 3 digits, optimizer runs to 5.
        self.assertAlmostEqual(
            pf.desired_portfolio.allocation_array[0], 0.481, 3)
        self.assertAlmostEqual(
            pf.desired_portfolio.allocation_array[1], 0.519, 3)
        self.assertAlmostEqual(
            pf.desired_portfolio.average_return, 1.001, 3)
        self.assertAlmostEqual(
            pf.desired_portfolio.downside_risk, 0.001, 3)
        self.assertAlmostEqual(
            pf.desired_portfolio.downside_correl, 0.044, 3)
        self.assertAlmostEqual(
            pf.desired_portfolio.score, 16.123, 3)


if __name__ == '__main__':
    unittest.main()

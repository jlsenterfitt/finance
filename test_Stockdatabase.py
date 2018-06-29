from collections import OrderedDict
from decimal import Decimal
import numpy as np
import unittest

import Config
from Stock import Stock
from StockDatabase import StockDatabase


class Test_StockDatabase(unittest.TestCase):
    def setUp(self):
        # Change the config value.
        Config.MINIMUM_AMOUNT_DATA = 4

        test_data = OrderedDict()
        test_data['2018-01-01'] = Decimal('101.00')
        test_data['2018-01-02'] = Decimal('102.00')
        test_data['2018-01-03'] = Decimal('103.00')
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
        test_data['2018-01-02'] = Decimal('303.00')
        test_data['2018-01-03'] = Decimal('306.00')
        test_data['2018-01-04'] = Decimal('309.00')
        stock3 = Stock(test_data, '3', 0)

        self.test_stock_dict = {'1': stock1, '2': stock2, '3': stock3}

    def test_filterStocks(self):
        stock_db = StockDatabase(self.test_stock_dict)
        self.assertItemsEqual(stock_db.stock_dict.keys(), ['2', '3'])

    def test_getFilteredPrices(self):
        stock_db = StockDatabase(self.test_stock_dict)
        # Stock 1 is filtered out, so rows should have stock2 + 3 data.
        self.assertListEqual(list(stock_db.price_array[0]), [200, 300])
        self.assertListEqual(list(stock_db.price_array[1]), [202, 303])
        self.assertListEqual(list(stock_db.price_array[2]), [206, 306])
        self.assertListEqual(list(stock_db.price_array[3]), [208, 309])
        self.assertEqual(len(stock_db.price_array), 4)

    def test_getCovarianceArray(self):
        stock_db = StockDatabase(self.test_stock_dict)
        expected = np.array([[2.20041322e-05, 7.37259266e-09],
                             [7.37259266e-09, 6.40800126e-09]])
        self.assertAlmostEqual(stock_db.covar_array()[0][0],
                               expected[0][0])
        self.assertAlmostEqual(stock_db.covar_array()[0][1],
                               expected[0][1])
        self.assertAlmostEqual(stock_db.covar_array()[1][0],
                               expected[1][0])
        self.assertAlmostEqual(stock_db.covar_array()[1][1],
                               expected[1][1])


if __name__ == '__main__':
    unittest.main()

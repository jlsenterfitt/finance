from collections import OrderedDict
from decimal import Decimal
import numpy as np
import unittest

import Config
from Stock import Stock


class Test_Stock(unittest.TestCase):
    def setUp(self):
        test_data = OrderedDict()
        test_data['2018-01-01'] = Decimal('100.00')
        test_data['2018-01-02'] = Decimal('101.00')
        test_data['2018-01-03'] = Decimal('102.00')
        test_data['2018-01-04'] = Decimal('103.00')
        test_data['2018-01-05'] = Decimal('104.00')
        self.stock = Stock(test_data, '', 0)

    def test_getPriceArray(self):
        expected = [100, 101, 102, 103, 104]
        self.assertListEqual(list(self.stock._price_array), expected)

    def test_getReturnArray(self):
        test_data = np.array(
            [100, 102, 103.02, 105.0804, 106.131204], dtype=np.float64)
        self.stock._price_array = test_data
        expected = [1.02, 1.01, 1.02, 1.01]
        self.assertListEqual(list(self.stock._getReturnArray()), expected)

    def test_getMeanAnnualReturn(self):
        test_data = np.array(
            [1.02, 1.01, 1.02, 1.01], dtype=np.float64)
        self.stock.return_array = test_data
        self.assertAlmostEqual(
            self.stock._getMeanAnnualReturn(),
            np.power(1.015, Config.DAYS_IN_YEAR))

    def test_getStDevAnnualReturn(self):
        test_data = np.array(
            [1.0, 3.0], dtype=np.float64)
        self.stock.return_array = test_data
        self.assertAlmostEqual(
            self.stock._getStDevAnnualReturn(),
            np.power(2, 0.5) * np.power(Config.DAYS_IN_YEAR, 0.5))

    def test_getConservativeAnnualReturn(self):
        self.stock._mean_annual_return = 1.01
        self.stock._st_dev_annual_return = 0.01
        self.stock.expense_ratio = Decimal('0.01')
        self.stock.return_array = range(4 * Config.DAYS_IN_YEAR)
        self.assertAlmostEqual(
            self.stock._getConservativeAnnualReturn(0.05), 0.9893473584)


if __name__ == '__main__':
    unittest.main()

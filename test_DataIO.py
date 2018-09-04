"""Handle testing of DataIO."""
import bz2
from collections import OrderedDict
import csv
from decimal import Decimal
import pickle
import os
from time import time
import unittest

import DataIO


class Test_getDesiredReturn(unittest.TestCase):
    def setUp(self):
        with open('data/test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Amount'])
            writer.writerow([1.06])

    def tearDown(self):
        os.remove('data/test.csv')

    def test(self):
        data = DataIO.getDesiredReturn('data/test.csv')
        self.assertAlmostEqual(float(data), 1.06)


class Test_getCurrentData(unittest.TestCase):
    def setUp(self):
        with open('data/test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Ticker', 'Amount'])
            writer.writerow(['CASH', 300.0])
            writer.writerow(['VTI', 100.0])

    def tearDown(self):
        os.remove('data/test.csv')

    def test(self):
        current_alloc_dict = DataIO.getCurrentData('data/test.csv')
        self.assertDictEqual(current_alloc_dict, {'CASH': 0.75, 'VTI': 0.25})


class Test_stringToDecimal(unittest.TestCase):
    def test_money(self):
        self.assertEqual(
            DataIO._stringToDecimal('-$123,456.78'), Decimal('-123456.78'))

    def test_percentage(self):
        self.assertEqual(
            DataIO._stringToDecimal('1.23%'), Decimal('0.0123'))


class Test_getTickerList(unittest.TestCase):
    def setUp(self):
        with open('data/test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Ticker', 'Expense'])
            writer.writerow(['CASH', '0.00%'])
            writer.writerow(['VTI', '0.1%'])

    def tearDown(self):
        os.remove('data/test.csv')

    def test(self):
        ticker_list, expense_ratio_dict = DataIO.getTickerList('data/test.csv')
        self.assertListEqual(ticker_list, ['CASH', 'VTI'])
        self.assertDictEqual(expense_ratio_dict, {
                             'CASH': Decimal('0'), 'VTI': Decimal('0.001')})


class Test_callApi(unittest.TestCase):
    def test(self):
        data = DataIO._callApi('VTI')
        first_date = data['VTI'].keys()[0]
        first_price = data['VTI'][first_date]
        timestamp = data['VTI']['_timestamp']
        self.assertListEqual(data.keys(), ['VTI'])
        self.assertRegexpMatches(first_date, '[0-9]{4}-[0-9]{2}-[0-9]{2}')
        self.assertIsInstance(first_price, Decimal)
        self.assertGreater(first_price, 0)
        # Time is to nearest second, so ensure we're roughly there.
        self.assertAlmostEqual(timestamp, time(), places=0)


class Test_getAPIData(unittest.TestCase):
    def test(self):
        data = DataIO._getAPIData(set(['VTI', 'QQQ']))
        self.assertListEqual(data.keys(), ['VTI', 'QQQ'])


class Test_storeCache(unittest.TestCase):
    def setUp(self):
        self.test_data = {'test_key': 'test_value'}

    def tearDown(self):
        os.remove('data/test.pkl.bz2')

    def test_noCache(self):
        DataIO._storeCache('data/test.pkl.bz2', self.test_data)
        with bz2.BZ2File('data/test.pkl.bz2', 'r') as f:
            raw_contents = f.read()
            contents = pickle.loads(raw_contents)
        self.assertDictEqual(contents, self.test_data)

    def test_prevCache(self):
        DataIO._storeCache('data/test.pkl.bz2', self.test_data)
        DataIO._storeCache('data/test.pkl.bz2', self.test_data)
        with bz2.BZ2File('data/test.pkl.bz2', 'r') as f:
            raw_contents = f.read()
            contents = pickle.loads(raw_contents)
        self.assertDictEqual(contents, self.test_data)


class Test_retrieveCache(unittest.TestCase):
    def setUp(self):
        self.filename = 'data/Test_retrieveCache.pkl.bz2'
        test_data = {
            'VTI': {'_timestamp': time(), '2018-01-01': 41.00},
            'QQQ': {'_timestamp': time() - 24 * 3600, '2018-01-01': 82.00}
        }
        DataIO._storeCache(self.filename, test_data)

    def test_withCache(self):
        contents = DataIO._retrieveCache(self.filename)
        # QQQ should be removed as outdated.
        self.assertListEqual(contents.keys(), ['VTI'])
        self.assertIsInstance(contents['VTI'], OrderedDict)
        os.remove(self.filename)

    def test_withoutCache(self):
        os.remove(self.filename)
        contents = DataIO._retrieveCache(self.filename)
        self.assertDictEqual(contents, {})


class Test_getRawData(unittest.TestCase):
    def setUp(self):
        self.filename = 'data/Test_getRawData.pkl.bz2'

    def tearDown(self):
        os.remove(self.filename)

    def test_withCache(self):
        test_data = {
            'VTI': {'_timestamp': time(), '2018-01-01': 41.00},
            'QQQ': {'_timestamp': 0, '2018-01-01': 82.00}
        }
        DataIO._storeCache(self.filename, test_data)

        raw_data = DataIO.getRawData(['VTI', 'QQQ'], self.filename)
        # Ensure all keys are present, even after removal of QQQ from cache.
        self.assertSequenceEqual(['VTI', 'QQQ'], raw_data.keys())
        # Ensure _timestamp was stripped.
        self.assertEqual('_timestamp' in raw_data['VTI'], False)
        self.assertEqual('_timestamp' in raw_data['QQQ'], False)
        # Ensure VTI matches what we cached.
        self.assertDictEqual(raw_data['VTI'], {'2018-01-01': 41.00})

    def test_withoutCache(self):
        DataIO.getRawData(['VTI', 'QQQ'], self.filename)
        # Ensure cache gets written.
        self.assertEqual(os.path.isfile(self.filename), True)


if __name__ == '__main__':
    unittest.main()

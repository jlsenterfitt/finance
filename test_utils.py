import unittest

import utils


class Test_getRequiredReturn(unittest.TestCase):
    def test_normal(self):
        expected = [1.1]
        actual = utils.getRequiredReturn([-110000], 100000)
        self.assertListEqual(actual, expected)

    def test_nan(self):
        expected = [0]
        actual = utils.getRequiredReturn([100000], 100000)
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

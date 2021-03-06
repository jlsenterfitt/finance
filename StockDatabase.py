from collections import OrderedDict
import datetime
import numpy as np

import Config


class StockDatabase(object):
    """Holds all Stock objects and related information."""

    def __init__(self, stock_dict):
        """Initialize the database.

        Args:
            stock_dict {dict}: Dict of stock objects.
        """
        self.stock_dict = stock_dict
        # Create a "standard" order of tickers.
        self.tickers = sorted(self.stock_dict.keys())
        self.price_array = self._getFilteredPrices()
        self.price_change_array = self._getPriceChangeArray()
        # TODO: Need to add CASH as a valid investment.

    def _getFilteredPrices(self):
        """Generate an array of all days with prices for every ticker.

        Some symbols may not have trading data on some days. This filters out
            those days, and creates and array of all prices and tickers.
        Returns:
            price_array {array}: Rows = Dates, Columns = Tickers
        """
        # Create dict of dates to tickers to prices.
        date_dict = {}
        for stock in self.stock_dict.values():
            for date in stock.ordered_date_dict.keys():
                if date not in date_dict:
                    date_dict[date] = {}
                date_dict[date][stock.ticker] = stock.ordered_date_dict[date]

        # Remove dates w/ missing tickers.
        for date in date_dict.keys():
            if len(date_dict[date].keys()) < len(self.stock_dict.keys()):
                del date_dict[date]
            elif datetime.datetime.strptime(date, '%Y-%m-%d') > Config.TODAY:
                del date_dict[date]

        # Order the dates.
        ordered_date_dict = OrderedDict(
            sorted(date_dict.items(), key=lambda t: t[0]))

        # Convert ordered date dict of prices, to the same thing in an array.
        # Rows = dates, columns = tickers, makes easier splicing.
        # Ticker order = self.tickers
        price_array = np.array([
            [
                ordered_date_dict[date][ticker]
                for ticker in self.tickers]
            for date in ordered_date_dict], dtype=np.float64)

        return price_array

    def _getPriceChangeArray(self):
        """Generate the array of price changes.

        Returns:
            price_change_array {array}: The percent changes of all prices.
        """
        prices = self.price_array[1:]
        prev_prices = self.price_array[:-1]
        raw_price_changes = prices / prev_prices
        expense_array = np.array(
            [self.stock_dict[ticker].expense_ratio for ticker in self.tickers], dtype=np.float64)
        expense_array = np.power(
            expense_array + 1.0, 1.0 / Config.DAYS_IN_YEAR) - 1.0
        expense_array = 1.0 - expense_array
        price_changes = raw_price_changes * \
            np.transpose(expense_array[:, None])
        return price_changes

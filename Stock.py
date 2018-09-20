import numpy as np
from scipy.stats import t
from scipy.stats.mstats import gmean

import Config


class Stock(object):
    """Represent a single stock and its performance."""

    def __init__(self, ordered_date_dict, ticker, expense_ratio):
        """Initialize major values.

        Args:
            ordered_data_dict {OrderedDict}: Dict of dates to prices, with dates
                in order.
            ticker {string}: Ticker of this stock.
        """
        self.ordered_date_dict = ordered_date_dict
        self.ticker = ticker
        self.expense_ratio = expense_ratio

        self._price_array = self._getPriceArray()
        self.return_array = self._getReturnArray()
        self._mean_annual_return = self._getMeanAnnualReturn()
        self._st_dev_annual_return = self._getStDevAnnualReturn()
        self.cons_annual_return = self._getConservativeAnnualReturn(
            Config.INITIAL_PERCENTILE)

    def _getPriceArray(self):
        """Extract the ordered_date_dict into an array of prices.

        Returns:
            price_array {Array}: Array of stock prices.
        """
        return np.array(
            self.ordered_date_dict.values(), dtype=np.float64)

    def _getReturnArray(self):
        """Convert price_array to an array of returns.

        Returns:
            return_array {Array}: Array of daily stock returns.
        """
        raw_price_array = self._price_array[1:] / self._price_array[:-1]
        daily_expense_ratio = np.power(float(1 + self.expense_ratio), 1.0 / Config.DAYS_IN_YEAR) - 1
        price_array = raw_price_array * float(1 - daily_expense_ratio)
        return price_array

    def _getMeanAnnualReturn(self):
        """Calculate the mean annual return from the return_array.

        Returns:
            mean_annual_return {float}: Artihmetic mean of daily stock returns,
                extrapolated out to one year.
        """
        return np.power(gmean(self.return_array), Config.DAYS_IN_YEAR)

    def _getStDevAnnualReturn(self):
        """Calculate the standard deviation of annual returns from return_array.

        Returns:
            st_dev_annual_return {float}: Standard deviation of annual returns,
                extrapoted out to one year.
        """
        return np.std(self.return_array, ddof=1) * np.power(Config.DAYS_IN_YEAR, 0.5)

    def _getConservativeAnnualReturn(self, p):
        """Calculate a conservative estimate of the annual return.

        Note: The t-distribution is used instead of the normal distribution, as
            I only assume that *years* are independent, not days. With a few
            years of data on a given stock (~10-20), this stops mattering, but
            for stocks with small amounts of data it means they'll take an
            outsized hit from their standard deviations.
        Args:
            p {float}: The percentile at which to estimate the return.
        Returns:
            cons_annual_return {float}: Lower bound of confidence interval for
                annual return using t distribution, mean return, and st dev
                return.
        """
        years_of_data = np.true_divide(
            len(self.return_array), Config.DAYS_IN_YEAR)
        t_value = t.ppf(p, years_of_data)
        initial_estimate = (self._mean_annual_return
                            + (t_value
                               * self._st_dev_annual_return
                               / np.power(years_of_data, 0.5)))
        return initial_estimate - initial_estimate * float(self.expense_ratio)

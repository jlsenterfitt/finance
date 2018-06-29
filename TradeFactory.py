class TradeFactory(object):
    """Gets a list of trades and their resulting effects on correlations."""

    def __init__(self, current_portfolio, desired_portfolio):
        """Initialize the factory.

        Args:
            current_portfolio {Portfolio}: Current investments and backtests.
            desired_portfolio {Portfolio}: Desired investments and backtests.
        """
        # TODO-implement
        pass

    def _getTradeList(self):
        """Generate a list of trades sorted by final correlation.

        For every combination (not permutation) of tickers, try to trade them
            and find the outcome correlation.
        Returns:
            trade_list {list}: List of sorted trades by correlation.
        """
        # TODO-implement
        pass
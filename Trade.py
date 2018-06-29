class Trade(object):
    """This represents a single potential trade.

    Its goal is to determine the correlation of the new portfolio with the
    desired portfolio after the trade.
    """
    def __init__(self, ticker1, ticker2, stock_db, curr_portfolio,
            desired_portfolio):
        """Initialize the Trade by calling internal init methods.

        Args:
            ticker1 {string}: The fisrt ticker to investigate.
            ticker2 {string}: The second ticker to investigate.
            stock_db {StockDatabase}: Database of all stock information.
            curr_portfolio {Portfolio}: Current investment portfolio.
            desired_portfolio {Portfolio}: Desired investment portfolio.
        """
        self._ticker1 = ticker1
        self._ticker2 = ticker2
        self._stock_db = stock_db
        self.curr_portfolio = curr_portfolio
        self._desired_portfolio = desired_portfolio

        # Which investment to buy.
        self.buy_ticker = None
        # Which investment to sell.
        self.sell_ticker = None
        # How much, in percentage points, to shift between buy and sell.
        self.trade_percentage = None
        # Correlation of hypothetical new portfolio with desired portfolio.
        self.new_correlation = None
        # TODO-implement
        pass

    def _getBuySellAndPercent(self):
        """Set the buy_ticker, sell_ticker, and trade_percentage.

        For a trade to occur, one ticker must be underweight and the other
            overweight. This sets the overweight to be sold, the underweight
            to be bought, and the lesser of how over- / underweight they are
            as the trade percentage.
        """
        # TODO-implement
        pass

    def _getNewCorrelation(self):
        """Determine the correlation after this trade with desired portfolio.
        
        Generates a new temporary portfolio with backtested returns.
        """
        # Use utils.
        # TODO-implement
        pass
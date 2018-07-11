import DataIO
from Portfolio import Portfolio
from Stock import Stock
from StockDatabase import StockDatabase
import utils


def getInputData():
    """Get all necessary input data for running a model.

    Returns:
        required_return_list {list}: Rate required to break even for each year.
        current_portfolio {Portfolio}: A Portfolio of current investments.
        stock_db {StockDatabase}: A database of all necessary stock info.
    """
    # Get future expenditures.
    cash_flow_list = DataIO.getFutureExpenditures('data/cashflows.csv')

    # Get current allocations.
    current_alloc_dict, funds_available = DataIO.getCurrentData(
        'data/current_allocations.csv')

    # Calculate IRR
    required_return_list = utils.getRequiredReturn(
        cash_flow_list, funds_available)

    # Get tickers and expense ratios.
    ticker_list, expense_ratio_dict = DataIO.getTickerList(
        'data/tickers_expenses.csv')

    # Get raw data.
    raw_data = DataIO.getRawData(ticker_list, 'data/cache.pkl.bz2')

    # Create all stock objects.
    stock_dict = {}
    for ticker in raw_data:
        stock_dict[ticker] = Stock(
            raw_data[ticker], ticker, expense_ratio_dict[ticker])

    # Create stock database.
    stock_db = StockDatabase(stock_dict)

    # Write stock database.
    DataIO.writeStockDatabase(stock_db, 'data/StockDatabase.csv')

    # Create current portfolio.
    current_portfolio = Portfolio(current_alloc_dict, stock_db)

    return required_return_list, current_portfolio, stock_db


def getDesiredPortfolio(required_return_list, stock_db):
    """Get the desired portfolio.

    Args:
        required_return_list {float}: Return required to pay bills.
        stock_db {StockDatabase}: A database of all necessary stock info.
    Returns:
        desired_portfolio {Portfolio}: A Portfolio with chosen weights.
    """
    # Iteratively create desired weights.
    # wf = WeightFactory.WeightFactory(stock_db, required_return_list)

    # Create desired portfolio.
    # desired_portfolio = Portfolio.Portfolio(wf.desired_alloc_dict, stock_db)

    return {}


def getTrades(current_portfolio, desired_portfolio):
    """Get a list of potential trades to get to a desired correlation.

    Args:
        current_portfolio {Portfolio}: A Portfolio of current investments.
        desired_portfolio {Portfolio}: A Portfolio with chosen weights.
    """
    # Create trade factory between current and desired portfolio.
    # tf = TradeFactory.TradeFactory(current_portfolio, desired_portfolio)

    # Print trade factory.
    # DataIO.writeTrades(trade_factory, filename)
    pass


def main():
    (required_return_list, current_portfolio, stock_db) = getInputData()

    desired_portfolio = getDesiredPortfolio(required_return_list, stock_db)

    getTrades(current_portfolio, desired_portfolio)


if __name__ == '__main__':
    main()

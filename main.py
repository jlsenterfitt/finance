import DataIO
from Portfolio import Portfolio
from PortfolioFactory import PortfolioFactory
from Stock import Stock
from StockDatabase import StockDatabase
import utils


def getInputData():
    """Get all necessary input data for running a model.

    Returns:
        required_return {float}: Rate required to break even for all years.
        current_portfolio {Portfolio}: A Portfolio of current investments.
        stock_db {StockDatabase}: A database of all necessary stock info.
    """
    # Get future expenditures.
    cash_flow_list = DataIO.getFutureExpenditures('data/cashflows.csv')

    # Get current allocations.
    current_alloc_dict, funds_available = DataIO.getCurrentData(
        'data/current_allocations.csv')

    # Calculate IRR
    required_return = utils.getRequiredReturn(cash_flow_list, funds_available)

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

    # Create current portfolio.
    current_portfolio = Portfolio(
        stock_db, percent_allocations_dict=current_alloc_dict)

    return required_return, current_portfolio, stock_db


def getTrades(current_portfolio, desired_portfolio):
    """Get a list of potential trades to get to a desired correlation.

    Args:
        current_portfolio {Portfolio}: A Portfolio of current investments.
        desired_portfolio {Portfolio}: A Portfolio with chosen weights.
    """
    # Create trade factory between current and desired portfolio.
    # tf = TradeFactory.TradeFactory(current_portfolio, desired_portfolio)

    return {}


def main():
    print('Reading data...')
    (required_return, current_portfolio, stock_db) = getInputData()

    # Write stock database.
    DataIO.writeStockDatabase(stock_db, 'data/StockDatabase.csv')

    print('Optimizing portfolio...')
    pf = PortfolioFactory(stock_db, required_return)
    desired_portfolio = pf.desired_portfolio
    print(stock_db.tickers)
    print(desired_portfolio.allocation_array)
    print(desired_portfolio.score)

    # Write desired portfolio.
    DataIO.writeDesiredPortfolio(
        desired_portfolio, 'data/DesiredPortfolio.csv')

    tf = getTrades(current_portfolio, desired_portfolio)

    # Print trade factory.
    DataIO.writeTrades(tf, 'data/Trades.csv')


if __name__ == '__main__':
    main()

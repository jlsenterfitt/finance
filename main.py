from multiprocessing import Pool

import DataIO
from Portfolio import Portfolio
from PortfolioFactory import PortfolioFactory
from Stock import Stock
from StockDatabase import StockDatabase


def getInputData():
    """Get all necessary input data for running a model.

    Returns:
        current_portfolio {Portfolio}: A Portfolio of current investments.
        stock_db {StockDatabase}: A database of all necessary stock info.
    """

    # Get current allocations.
    current_alloc_dict = DataIO.getCurrentData('data/current_allocations.csv')

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

    return current_portfolio, stock_db


def getTrades(current_portfolio, desired_portfolio):
    """Get a list of potential trades to get to a desired correlation.

    Args:
        current_portfolio {Portfolio}: A Portfolio of current investments.
        desired_portfolio {Portfolio}: A Portfolio with chosen weights.
    """
    # Create trade factory between current and desired portfolio.
    # tf = TradeFactory.TradeFactory(current_portfolio, desired_portfolio)

    return {}


def optimizeForReturn(iteration, stock_db):
    """Optimize and write a solution for a given return.

    Args:
        iteration (int): Which iteration to run.
        stock_db {StockDatabase}: A database of all necessary stock info.
    """
    required_return = 1 + (iteration / 100.0)

    print('Optimizing portfolio for %.2f' % required_return)
    pf = PortfolioFactory(stock_db, required_return)
    desired_portfolio = pf.desired_portfolio
    print('IRR: %f' % required_return)
    print('Score: %f' % desired_portfolio.score)

    # Write desired portfolio.
    DataIO.writeDesiredPortfolio(
        desired_portfolio, stock_db, 'data/DesiredPortfolio_%d.csv' % iteration)

    print('Finished for %.2f' % required_return)


def main():
    pool = Pool()
    print('Reading data...')

    # Get initial data.
    current_portfolio, stock_db = getInputData()

    # Write stock database.
    DataIO.writeStockDatabase(stock_db, 'data/StockDatabase.csv')

    results = []
    for i in xrange(10):
        results.append(pool.apply_async(optimizeForReturn, (i, stock_db)))

    for result in results:
        result.wait(600)

    # tf = getTrades(current_portfolio, desired_portfolio)

    # Print trade factory.
    # DataIO.writeTrades(tf, 'data/Trades.csv')


if __name__ == '__main__':
    main()

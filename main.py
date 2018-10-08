import argparse
import datetime
import math

import Config
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
    raw_data = DataIO.getRawData(ticker_list)

    # Create all stock objects.
    stock_dict = {}
    for ticker in raw_data.keys():
        stock_dict[ticker] = Stock(
            raw_data[ticker], ticker, expense_ratio_dict[ticker])

    if not len(stock_dict.keys()):
        raise ValueError('No keys found.')

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


def optimizeForReturn(required_return, stock_db, use_genetic):
    """Optimize and write a solution for a given return.

    Args:
        required_return (float): What return to require.
        stock_db {StockDatabase}: A database of all necessary stock info.
    """
    print('Optimizing portfolio for %f' % required_return)
    pf = PortfolioFactory(stock_db, required_return, use_genetic=use_genetic)
    desired_portfolio = pf.desired_portfolio
    print('Required Return: %f' % required_return)
    print('Expected Return: %f' % math.pow(
        desired_portfolio.average_return, Config.DAYS_IN_YEAR))
    print('Downside Risk: %f' % desired_portfolio.downside_risk)
    print('Downside Correl: %f' % desired_portfolio.downside_correl)
    print('Score: %f' % desired_portfolio.score)

    # Write desired portfolio.
    DataIO.writeDesiredPortfolio(
        desired_portfolio, stock_db,
        'output/DesiredPortfolio_%.0f_%.4f_%s.csv' % (
            Config.MINIMUM_AMOUNT_DATA, required_return, Config.TODAY.date()))

    print('Finished for %f' % required_return)

    return desired_portfolio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--desired_return', type=float,
                        help='The desired return.')
    parser.add_argument('--num_years', type=float,
                        help='Number of years of data to require.')
    parser.add_argument('--solve', dest='solve', action='store_true')
    parser.add_argument('--no-solve', dest='solve', action='store_false')
    parser.add_argument('--set_date', type=str, help='Some date to run as')
    parser.add_argument('--use_genetic', dest='use_genetic',
                        action='store_true')
    parser.set_defaults(solve=True)
    parser.set_defaults(use_genetic=False)
    args = parser.parse_args()
    required_return = args.desired_return

    if not args.desired_return and args.solve:
        raise ValueError('Desired return or no-solve must be specified.')

    if args.set_date:
        Config.TODAY = datetime.datetime.strptime(
            args.set_date, '%Y-%m-%d')

    if args.num_years:
        Config.MINIMUM_AMOUNT_DATA = Config.DAYS_IN_YEAR * args.num_years

    print('Reading data...')

    # Get initial data.
    current_portfolio, stock_db = getInputData()

    # Write stock database.
    DataIO.writeStockDatabase(stock_db, 'output/StockDatabase.csv')

    if not args.solve:
        return

    desired_portfolio = optimizeForReturn(
        required_return, stock_db, args.use_genetic)

    tf = getTrades(current_portfolio, desired_portfolio)

    # Print trade factory.
    DataIO.writeTrades(tf, 'data/Trades.csv')


if __name__ == '__main__':
    main()

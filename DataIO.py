"""This module handles all data IO.

That includes caching, API calls, file reading, etc."""

import bz2
from collections import OrderedDict
import csv
import datetime
from decimal import Decimal
import os
import cPickle as pickle
import math
from multiprocessing.dummy import Pool
from re import sub
import requests
from time import sleep, time

import Config

# TODO: Update cache mechanism.
# Tickers should be written individually to a cache folder as JSON objects w/ timestamps.
# Still discard any tickers w/o timestamps.

# Config options.
last_request_time = time()
local_cache = {}


def getTickerList(filename):
    """Read a file with a list of tickers to check.

    Args:
        filename {str}: A path to the correct file.
    Returns:
        ticker_list {list}: List of ticker symbols.
        expense_ratio_dict {dict}: Dict of tickers to expense ratios.
    """
    ticker_list = []
    expense_ratio_dict = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        reader.next()  # Header
        for row in reader:
            ticker = row[0]
            ticker = sub(r'[^A-Z]', '-', ticker)
            expense = _stringToDecimal(row[1])
            ticker_list.append(ticker)
            expense_ratio_dict[ticker] = expense
    return ticker_list, expense_ratio_dict


def getRawData(ticker_list, use_cache=True):
    """Check for valid cache data, or get raw stock data via API and cache it.

    First loads the cache, then strips any outdated data.
    Calls the API for any missing (or removed) data.
    Stores the new data in the cache.
    Strips the data of _timestamp entries, and returns the result.
    Args:
        ticker_list {list}: List of ticker symbols.
        use_cache {boolean}: Whether to use the saved cache.
    Returns:
        raw_data {dict}: dict of tickers to dates to prices.
    """
    if use_cache:
        cache_data = _retrieveCacheFiles(ticker_list)
    else:
        cache_data = {}
    for ticker in cache_data.keys():
        if cache_data[ticker] == 'too_short':
            del cache_data[ticker]
            ticker_list.remove(ticker)
    available_keys = sorted(
        cache_data.keys(), key=lambda ticker: cache_data[ticker]['_timestamp'])
    # Hack: Remove oldest tickers to slowly refresh cache throughout day.
    for _ in xrange(int(math.ceil(len(available_keys) / 100.0))):
        del available_keys[0]
    # Determine missing keys and call API for them.
    missing_tickers = set(ticker_list).difference(set(available_keys))
    print('Getting %d missing tickers.' % len(missing_tickers))
    # Hack: To get the cache to store after each API call, I'm passing the
    # tickers once at a time. I could refactor, but I'm feeling lazy.
    cache_data.update(_getAPIData(missing_tickers))
    for ticker in cache_data:
        if '_timestamp' in cache_data[ticker]:
            del cache_data[ticker]['_timestamp']
    return cache_data


def getCurrentData(filename):
    """Get current investment information.

    Args:
        filename {string}: Where the current investment data is stored.
    Returns:
        current_alloc_dict {dict}: Dict of tickers to percentage allocations.
    """
    current_alloc_dict = {}
    funds_available = Decimal()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        reader.next()  # Header
        for row in reader:
            amount = _stringToDecimal(row[1])
            current_alloc_dict[row[0]] = amount
            funds_available += amount
    # Convert dollar amounts to percentages.
    for ticker in current_alloc_dict:
        current_alloc_dict[ticker] = (
            current_alloc_dict[ticker] / funds_available)
    return current_alloc_dict


def getDesiredReturn(filename):
    """Read desired return.

    Args:
        filename {string}: Where the data is stored.
    Returns:
        desired_return {float}: The desired return as a float
            (e.g., 1.06 for a 6% return).
    """
    raw_data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        reader.next()  # Header
        for row in reader:
            raw_data.append(_stringToDecimal(row[0]))
    if len(raw_data) > 1:
        raise ValueError('Should only have 2 rows, a header and a value.')
    return float(raw_data[0])


def writeTrades(trade_factory, filename):
    """Write the desired trades to disk.

    Args:
        trade_factory {TradeFactory}: The data to write.
        filename {string}: Where to write the data.
    """
    # TODO-implement
    pass


def writeDesiredPortfolio(portfolio, stock_db, filename):
    """Write the desired portfolio to disk.

    Args:
        portfolio {Portfolio}: The portfolio to write.
        stock_db {StockDatabase}: Database of stock information.
        filename {string}: Where to write the data.
    """
    output_data = []
    for i, ticker in enumerate(stock_db.tickers):
        output_data.append([ticker, portfolio.allocation_array[i]])

    sorted_output_data = sorted(output_data, key=lambda a: a[1], reverse=True)
    sorted_output_data.insert(0, ['Ticker', 'Allocation'])

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted_output_data)


def writeStockDatabase(stock_db, filename):
    """Write the database to disk.

    Args:
        stock_db {StockDatabase}: The data to write.
        filename {string}: Where to write the data.
    """
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Ticker',
            'Expense Ratio',
            'Mean Annual Return',
            'St. Dev. Annual Return',
            'Cons. Annual Return'
        ])
        for ticker in stock_db.tickers:
            stock = stock_db.stock_dict[ticker]
            new_row = [
                ticker,
                stock.expense_ratio,
                stock._mean_annual_return,
                stock._st_dev_annual_return,
                stock.cons_annual_return
            ]
            writer.writerow(new_row)


def _retrieveCache(filename):
    """Pull data from a specific cache file.

    Args:
        filename {string}: Name of the cache file to read.
    Returns:
        contents {dict}: Dict of tickers to dates to prices. Each ticker also
            has a _timestamp entry saying when it was pulled.
    """
    output = {}
    try:
        full_name = 'cache_files/' + filename
        with bz2.BZ2File(full_name, 'r') as f:
            raw_contents = f.read()
            try:
                contents = pickle.loads(raw_contents)
                if contents['_timestamp'] < time() - 31 * 24 * 60 * 60:
                    return {}
            except KeyError:
                raise IOError
        for date in contents:
            if date == '_timestamp':
                continue
            if datetime.datetime.strptime(date, '%Y-%m-%d') > Config.TODAY:
                del contents[date]
            elif contents[date] < 0.01:
                del contents[date]
        ticker = filename.split('.')[0]
        output = {}
        if len(contents.keys()) < Config.MINIMUM_AMOUNT_DATA:
            output[ticker] = 'too_short'
            return output
        output[ticker] = OrderedDict(
            sorted(contents.items(), key=lambda t: t[0]))
    except IOError:
        pass
    return output


def _retrieveCacheFiles(ticker_list):
    """Retrieve valid cache files.

    Returns:
        cache_data {dict}: Dict of tickers to dates to prices. Each ticker also
            has a _timestamp entry saying when it was pulled.
    """
    filenames = os.listdir('./cache_files')
    # Remove any files we aren't actively looking for.
    filenames = [filename for filename in filenames if filename.split('.')[
        0] in ticker_list]
    output = {}
    pool = Pool()
    content_dicts = pool.map(_retrieveCache, filenames, int(
        math.ceil(math.sqrt(len(filenames)))))
    pool.close()
    for content_dict in content_dicts:
        output.update(content_dict)
    return output


def _storeCache(filename, cache_data):
    """Write the cache to disk.

    Args:
        filename {string}: Where to write the file.
        cache_data {dict}: What data to write.
    """
    data_pkl = pickle.dumps(cache_data)
    with bz2.BZ2File(filename, 'wb') as f:
        f.write(data_pkl)


def _getAPIData(ticker_list):
    """Call the API to get raw price data.

    Args:
        ticker_list {list}: List of tickers we need data for.
    Returns:
        cache_data {dict}: Dict of tickers to dates to prices. Each ticker also
            has a _timestamp entry saying when it was pulled.
    """
    cache_data = {}
    for t, ticker in enumerate(ticker_list):
        print('Retrieving ticker %d of %d (%s)' %
              (t + 1, len(ticker_list), ticker))
        cache_data.update(_callApi(ticker))
        _storeCache('cache_files/' + ticker + '.pkl.bz2', cache_data[ticker])
        for date in cache_data[ticker]:
            if date == '_timestamp':
                continue
            if datetime.datetime.strptime(date, '%Y-%m-%d') > Config.TODAY:
                del cache_data[ticker][date]
            elif cache_data[ticker][date] <= 0.01:
                del cache_data[ticker][date]
        if len(cache_data[ticker].keys()) < Config.MINIMUM_AMOUNT_DATA:
            del cache_data[ticker]
    return cache_data


def _callApi(ticker):
    """Call the API for data about a single ticker.

    Args:
        ticker {string}: The ticker to get data for.
    Returns:
        cache_data {dict}: Dict of tickers to dates to prices. Each ticker also
            has a _timestamp entry saying when it was pulled.
    """
    global last_request_time
    global local_cache
    if ticker in local_cache:
        return local_cache[ticker]
    result = {}
    # Track the number of 503s in case the server is down for an extended period.
    count_503s = 0
    attempts = 0
    while 'Time Series (Daily)' not in result and attempts < 120:
        attempts += 1
        sleep(max(
            0,
            Config.MIN_TIME_BETWEEN_CALLS - (time() - last_request_time)))
        raw_result = requests.get(Config.BASE_REQUEST + ticker)
        last_request_time = time()
        try:
            if raw_result.status_code == 503:
                count_503s += 1
                if count_503s >= 60:
                    raise IOError('Too many 503s from API.')
                continue
            result = raw_result.json()
        except ValueError as e:
            print(raw_result)
            raise e

    if attempts >= 120:
        raise IOError('Could not get ticker %s' % ticker)

    # Extract the date-price pairs.
    data = {}
    for date in result['Time Series (Daily)']:
        data[date] = _stringToDecimal(
            result['Time Series (Daily)'][date]['5. adjusted close'])

    # Convert the date-dict to an ordered one.
    ordered_date_dict = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    cache_data = {ticker: ordered_date_dict}
    cache_data[ticker].update({'_timestamp': time()})

    local_cache[ticker] = cache_data

    return cache_data


def _stringToDecimal(string_money):
    """Convert money formatted as a string (e.g., -$170,000) to a Decminal

    Args:
        string_money {string}: Money formatted as a string, e.g., "-$147,000.00"
    Returns:
        amount {Decimal}: The money converted to a Decimal.
    """
    is_decimal = string_money.endswith('%')
    raw_amount = Decimal(sub(r'[^\d\.\-]', '', string_money))
    if is_decimal:
        raw_amount /= Decimal('100.0')
    return raw_amount

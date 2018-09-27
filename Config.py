"""File for global configuration."""
import datetime

DAYS_IN_YEAR = 261
INITIAL_PERCENTILE = 0.5

TODAY = datetime.datetime.today()


def SetMinData():
    # This forces us to only use tickers that were around during the dot-com bust.
    # Over time it will become more stringent, capping at requiring 21 years of data.
    # 21 years of data should include 2-3 major recessions.
    global MINIMUM_AMOUNT_DATA
    MIN_YEARS = min(
        (TODAY.date() - datetime.date(1984, 1, 1)).days / (2.0 * 365),
        21)
    MINIMUM_AMOUNT_DATA = MIN_YEARS * DAYS_IN_YEAR


SetMinData()

with open('api_key_ignore_.txt', 'r') as f:
    API_KEY = f.read()
SIZE = 'full'  # compact|full
MIN_TIME_BETWEEN_CALLS = 1.0
BASE_REQUEST = (
    'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=' +
    API_KEY + '&outputsize=' + SIZE + '&symbol=')

"""File for global configuration."""
import datetime

DAYS_IN_YEAR = 261
INITIAL_PERCENTILE = 0.5

TODAY = datetime.datetime.today()
MINIMUM_AMOUNT_DATA = 8 * DAYS_IN_YEAR

with open('api_key_ignore_.txt', 'r') as f:
    API_KEY = f.read()
SIZE = 'full'  # compact|full
MIN_TIME_BETWEEN_CALLS = 1.0
BASE_REQUEST = (
    'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=' +
    API_KEY + '&outputsize=' + SIZE + '&symbol=')

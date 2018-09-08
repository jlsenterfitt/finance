"""File for global configuration."""
import datetime

DAYS_IN_YEAR = 261
INITIAL_PERCENTILE = 0.5

# Gives 14 years as of 2018, 21 years as of 2032.
MIN_YEARS = min(
    (datetime.date.today() - datetime.date(1990, 1, 1)).days / (2.0 * 365),
    21)
MINIMUM_AMOUNT_DATA = MIN_YEARS * DAYS_IN_YEAR

with open('api_key_ignore_.txt', 'r') as f:
    API_KEY = f.read()
SIZE = 'full'  # compact|full
MIN_TIME_BETWEEN_CALLS = 1.0
BASE_REQUEST = (
    'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=' +
    API_KEY + '&outputsize=' + SIZE + '&symbol=')

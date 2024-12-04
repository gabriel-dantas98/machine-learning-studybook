import yfinance as yf
from core.observability import tracer
from core.observability import logger

class YahooFinance: 
    def collect_data(self, symbol, start_date, end_date):
        with tracer.start_as_current_span("collect_data"):
            logger.info(f"Collecting data for symbol: {symbol}, between {start_date} and {end_date}")
            df = yf.download(symbol, start=start_date, end=end_date)
            logger.info(f"Data collected: {len(df)} records found.")
        return df

import os
import finnhub
from dotenv import load_dotenv
import logging
from datetime import datetime
import argparse
import pytz


# Load API key from .env
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validate API key
if not API_KEY:
    logging.error("API key is missing. Ensure it is set in the .env file.")
    exit(1)

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key=API_KEY)

def fetch_real_time_data(symbol):
    """
    Fetch real-time cryptocurrency data.
    :param symbol: Cryptocurrency pair (e.g., 'BINANCE:BTCUSDT')
    :return: Dictionary containing real-time data.
    """
    try:
        data = finnhub_client.quote(symbol)
        # logging.info(f"Successfully fetched real-time data for {symbol}")
        return data
    except finnhub.exceptions.FinnhubAPIException as e:
        logging.error(f"API error while fetching data for {symbol}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for {symbol}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch real-time cryptocurrency data.")
    parser.add_argument("--symbol", type=str, default="BINANCE:BTCUSDT", help="Cryptocurrency pair (default: BINANCE:BTCUSDT)")
    args = parser.parse_args()

    real_time_data = fetch_real_time_data(args.symbol)
    if real_time_data:
        print(f"Data fetched at {datetime.now()} ")
        print(real_time_data)
    else:
        print(f"Failed to fetch real-time data for {args.symbol}")

import time
from datetime import datetime
import logging
from data_fetching import fetch_real_time_data
from data_processing import process_crypto_data
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_process(symbol):
    """
    Fetch, process, and print real-time cryptocurrency data.
    :param symbol: Cryptocurrency pair (e.g., 'BINANCE:BTCUSDT').
    """
    # logging.info(f"Fetching data for {symbol}...")

    # Fetch real-time data
    raw_data = fetch_real_time_data(symbol)
    # print(raw_data)
    if raw_data:
        # Convert raw dictionary data into a DataFrame
        raw_df = pd.DataFrame([raw_data])
        raw_df.rename(columns={
            'c': 'close',
            'd': 'price_change',
            'dp': 'percent_change',
            'h': 'high',
            'l': 'low',
            'o': 'open',
            'pc': 'previous_close',
            't': 'timestamp'
        }, inplace=True)
        raw_df['timestamp'] = pd.to_datetime(raw_df['timestamp'], unit='s')+ pd.Timedelta(hours=24)

        # Process the raw data
        processed_df = process_crypto_data(raw_df)

        # Print the processed data
        # print(f"\nProcessed Data at {datetime.utcnow()} UTC:")
        print(processed_df)

        # Save processed data to a CSV
        file_name = 'processed_crypto_data.csv'
        processed_df.to_csv(file_name, mode='a', index=False, header=not pd.io.common.file_exists(file_name))
        # logging.info(f"Processed data saved to {file_name}")
    else:
        logging.error(f"Failed to fetch data for {symbol}.")

if __name__ == "__main__":
    symbol = 'BINANCE:BTCUSDT'

    # Schedule: Fetch and process every 60 seconds (can be adjusted)
    interval = 10  # seconds

    logging.info("Starting automatic data fetching and processing...")
    try:
        while True:
            fetch_and_process(symbol)
            # logging.info(f"Waiting {interval} seconds before the next fetch...")
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Automatic fetching and processing stopped by user.")

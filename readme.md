## Requirements
- Python 3.x
- Required libraries listed in `requirements.txt`

## Setup Instructions
1. **Create a Virtual Environment:**
   It is recommended to run the program in a virtual environment.
   ```bash
   python -m venv <directory>
   ```

2. **Activate the Virtual Environment:**
   - **Windows:**
     ```bash
     <directory>\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source <directory>/bin/activate
     ```

3. **Install the Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the Whole Directory is Present:**
   Make sure to run the file via the directory/open directory in terminal or IDE.

5. **Enter API Key:**
   Enter your API key from FinHub into `FINHUB_API_KEY.txt`.

6. **Change Coin Symbol:**
   Modify the coin symbol in `scripts/data_writing.py` line 51, e.g., `'BINANCE:BTCUSDT'`.

7. **Optional: Display Additional Stats:**
   `scripts/data_writing.py` line 37 is optional, used to display additional stats (not used for ML tasks). Comment out when writing data for ML.

8. **Change Frequency of Data Fetching:**
   Adjust the frequency of data fetching in `scripts/data_writing.py` line 54.

## Running the Program
When the `data_writing.py` starts running, `processed_crypto_data.csv` will start updating.

## Visualization
1. **Change Target Timezone:**
   Change the target timezone in `scripts/data_visualization.py` line 13.

2. **Run the Visualization Script:**
   Run the file and open the port given in the terminal to view live visualization.

## Jupyter Notebooks
There are Jupyter notebooks in the `ML` directory:
- **Cleaning:** Used just for cleaning data, not necessary for ML.
- **XGB:** Better at detecting dips in the data.
- **LTSM:** Better for detecting highs.

Run each notebook to view results.

## Notes
- The models are not optimized for live data.
'''

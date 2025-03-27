# BTC Price and Box Cox Puell Multiple

This script fetches Bitcoin (BTC) price data and the Puell Multiple data, merges them into a single dataset, and visualizes the Box-Cox transformation of the Puell Multiple alongside BTC price over time. The goal of this indicator is to identify potential overbought and oversold zones within the typical 4 year cycle of Bitcoin.

Historical performance:
![image](https://github.com/user-attachments/assets/dd7ea71d-82dd-4d4f-8a7a-f867642d230a)


## Features
- Fetches BTC price and Puell Multiple data from APIs.
- Merges and processes data into a single dataset.
- Filters data to start from a specified date (`2014-01-01` by default).
- Generates a visualization of the Puell Multiple and BTC price over time.

---

## Installation

### Prerequisites
- Python 3.7 or later.
- Ensure `pip` is installed on your system.

### Steps

#### MacOS
1. **Install Python**:
   - Use Homebrew:
     ```bash
     brew install python
     ```

2. **Install required libraries**
   ```
   pip install pandas numpy matplotlib requests scipy
   ```

3. **Run the Script**
   ```
   python btc_aviv_analysis.py
   ```

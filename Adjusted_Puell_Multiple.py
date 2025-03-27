#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Function to fetch the list of BTC prices from the API
def fetch_btc_price_list():
    url = 'https://bitcoin-data.com/api/v1/btc-price'  # Replace with the actual API endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to fetch the MVRV Ratio from the API
def fetch_puell_multiple_list():
    url = 'https://bitcoin-data.com/api/v1/puell-multiple'  # Updated endpoint for MVRV Ratio
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            print("Unexpected data format or empty list.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def merge_btc_and_puell_multiple(btc_price_data, puell_multiple_data):
    """
    Merges BTC Price data and Puell Multiple data into a pandas DataFrame, 
    truncating the time to start at the beginning of 2012.

    Parameters:
        btc_price_data (list of dict): List of BTC price data with keys 'd', 'unixTs', and 'btcPrice'.
        puell_multiple_data (list of dict): List of Puell Multiple data with keys 'd', 'unixTs', and 'puellMultiple'.

    Returns:
        pd.DataFrame: Merged DataFrame with columns 'DateTime', 'BTC price', and 'Puell Multiple'.
    """
    # Convert to pandas DataFrames
    btc_df = pd.DataFrame(btc_price_data).rename(columns={'d': 'DateTime', 'btcPrice': 'BTC price'})
    puell_df = pd.DataFrame(puell_multiple_data).rename(columns={'d': 'DateTime', 'puellMultiple': 'Puell Multiple'})

    # Merge dataframes on 'DateTime'
    merged_df = pd.merge(btc_df[['DateTime', 'BTC price']], puell_df[['DateTime', 'Puell Multiple']], on='DateTime')

    # Convert 'DateTime' to datetime format and ensure numeric data
    merged_df['DateTime'] = pd.to_datetime(merged_df['DateTime'])
    merged_df['BTC price'] = pd.to_numeric(merged_df['BTC price'])
    merged_df['Puell Multiple'] = pd.to_numeric(merged_df['Puell Multiple'])

    # Filter to include only dates from the beginning of 2012 onward
    start_date = pd.Timestamp('2014-01-01')
    merged_df = merged_df[merged_df['DateTime'] >= start_date]

    return merged_df
        
# Apply Box-Cox and Z-score
def apply_boxcox_and_zscore(df):
    puell_positive = df['Puell Multiple'] + 1e-5
    df['Box-Cox Puell Multiple'], _ = boxcox(puell_positive)
    df['Z-score Box-Cox Puell Multiple'] = (
        df['Box-Cox Puell Multiple'] - df['Box-Cox Puell Multiple'].mean()
    ) / df['Box-Cox Puell Multiple'].std()
    return df

# Plotting function
def plot_btc_and_puell(df):
    df['Log10 BTC Price'] = np.log10(df['BTC price'])
    df = df.iloc[:-1]
    df = df[df['DateTime'] >= pd.Timestamp('2015-01-01')]
    top_threshold = df['Z-score Box-Cox Puell Multiple'].quantile(0.975)
    bottom_threshold = df['Z-score Box-Cox Puell Multiple'].quantile(0.025)

    fig, ax1 = plt.subplots(figsize=(14, 8))

    for date in df['DateTime'][df['Z-score Box-Cox Puell Multiple'] >= top_threshold]:
        ax1.axvline(x=date, color='red', linestyle='-', alpha=0.5, zorder=1)
    for date in df['DateTime'][df['Z-score Box-Cox Puell Multiple'] <= bottom_threshold]:
        ax1.axvline(x=date, color='green', linestyle='-', alpha=0.5, zorder=1)

    ax1.set_xlabel('DateTime')
    ax1.set_ylabel('BTC Price', color='orange')
    ax1.plot(df['DateTime'], df['Log10 BTC Price'], color='orange', label='BTC Price', zorder=2)
    ax1.tick_params(axis='y', labelcolor='orange')
    ax1.set_yticks([1, 2, 3, 4])
    ax1.set_yticklabels([10, 100, 1000, 10000])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Box-Cox Puell Multiple', color='blue')
    ax2.plot(df['DateTime'], df['Z-score Box-Cox Puell Multiple'], color='blue', label='Box-Cox Puell Multiple', zorder=2)
    ax2.tick_params(axis='y', labelcolor='blue')

    fig.suptitle('BTC Box-Cox Puell Multiple', fontsize=16)
    custom_handles = [
        plt.Line2D([0], [0], color='orange', lw=2, label='BTC Price'),
        plt.Line2D([0], [0], color='blue', lw=2, label='Box-Cox Puell Multiple'),
        plt.Line2D([0], [0], color='red', lw=2, label='Z > 1.96 (Overbought)'),
        plt.Line2D([0], [0], color='green', lw=2, label='Z < -1.96 (Oversold)')
    ]
    plt.legend(handles=custom_handles, loc='upper left')

    plt.tight_layout()
    plt.show()

btc_price = fetch_btc_price_list()
puell_multiple_data = fetch_puell_multiple_list()
merged_df = merge_btc_and_puell_multiple(btc_price, puell_multiple_data)
merged_df = apply_boxcox_and_zscore(merged_df)
plot_btc_and_puell(merged_df)


# In[ ]:





import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_stock_news(tickers):
    """
    Fetches news data from finviz for the given stock tickers.

    Args: 
        tickers (list): List of stock tickers.

    Returns: 
        DataFrame: A DataFrame with columns ['ticker', 'date', 'time', 'title'].
    """

    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    headers = {'user-agent': 'my-app'}
    
    for ticker in tickers:
        try:
            url = finviz_url + ticker
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            html = BeautifulSoup(response.content, 'html.parser')
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table
        except Exception as e:
            print(f"Could not fetch data for {ticker}: {e}")
    
    parsed_data = []

    for ticker, news_table in news_tables.items():
        cur_date = None
        if news_table:  # Check if news_table is not None
            for row in news_table.findAll('tr'):
                title = row.a.text if row.a else ''
                date_data = row.td.text.strip().split(' ') if row.td else []

                if len(date_data) != 1:
                    date = date_data[0]
                    time = date_data[1]
                    cur_date = date
                else:
                    time = date_data[0]
                    date = cur_date

                parsed_data.append([ticker, date, time, title])
    
    return pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

# Example usage
#tickers = ['AMZN', 'GOOG', 'META']
#df = fetch_stock_news(tickers)
#print(df)

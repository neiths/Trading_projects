from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_stock_news(tickers):

    """Fetches news data from finviz for the given stock tickers.
    Args: list of stock tickers
    Returns: DataFrame with columns ['ticker', 'date', 'time', 'title']
    """

    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    
    for ticker in tickers:
        try:
            url = finviz_url + ticker
            req = Request(url=url, headers={'user-agent': 'my-app'})
            response = urlopen(req)
            html = BeautifulSoup(response, 'html.parser')
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table
        except:
            pass
    
    parsed_data = []

    for ticker, news_table in news_tables.items():
        cur_date = None
        for row in news_table.findAll('tr'):
            title = row.a.text
            date_data = row.td.text.strip().split(' ')

            if len(date_data) != 1:
                date = date_data[0]
                time = date_data[1]
                cur_date = date
            else:
                time = date_data[0]
                date = cur_date
            
            parsed_data.append([ticker, date, time, title])
    
    df =  pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

    #df['date'] = pd.to_datetime(df.date).dt.date

    #df['time'] = pd.to_datetime(df.time, format='%I:%M%p').dt.strftime('%H:%M')
    
    return df


# Example usage
#tickers = ['AAPL', 'AMZN', 'GOOGL']
#df = fetch_stock_news(tickers)
#print(df)

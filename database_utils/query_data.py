from typing import List, Tuple
import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

def get_ohlc_data(read_api, stock_code: str, from_date: int):
    """
    Fetches OHLC data from InfluxDB for a given stock code starting from a specified date.

    :param read_api: The InfluxDBClient API instance used to query the database.
    :param stock_code: The stock code to query.
    :param from_date: The starting date to fetch data from.
    :return: A DataFrame containing the OHLC data.
    """
    # Define the InfluxDB query
    query = f"""
    from(bucket: "your_bucket_name")
        |> range(start: -{from_date}d)
        |> filter(fn: (r) => r["_measurement"] == "ohlc")
        |> filter(fn: (r) => r["stock_code"] == "{stock_code}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> drop(columns: ["_start", "_stop"])
    """
    
    # Execute the query and get the result as a DataFrame
    result = read_api.query_data_frame(query)

    # Ensure the DataFrame is sorted by time
    result = result.sort_values('_time')

    # Rename columns to match the OHLC format
    result.rename(columns={'_time': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
    
    # Set the Date column as the index
    result.set_index('Date', inplace=True)

    return result

# Example usage
if __name__ == "__main__":
    db_path = 'path_to_your_database.db'
    ohlc_table_name = 'ohlc_table'
    order_flow_table_name = 'order_flow_table'
    
    ohlc_data = get_ohlc_data(db_path, ohlc_table_name)
    print("OHLC Data:", ohlc_data)
    

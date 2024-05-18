import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self, data):
        """
        Initialize with stock data.
        
        :param data: pandas DataFrame with columns 'Date' and 'Close'
        """
        self.data = data
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index('Date', inplace=True)

    def SMA(self, window):
        """
        Calculate Simple Moving Average (SMA).
        
        :param window: int, the window size for SMA
        :return: pandas Series with SMA values
        """
        return self.data['Close'].rolling(window=window).mean()

    def EMA(self, window):
        """
        Calculate Exponential Moving Average (EMA).
        
        :param window: int, the window size for EMA
        :return: pandas Series with EMA values
        """
        return self.data['Close'].ewm(span=window, adjust=False).mean()

    def RSI(self, window=14):
        """
        Calculate Relative Strength Index (RSI).
        
        :param window: int, the window size for RSI
        :return: pandas Series with RSI values
        """
        delta = self.data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def MACD(self, fast_window=12, slow_window=26, signal_window=9):
        """
        Calculate Moving Average Convergence Divergence (MACD).
        
        :param fast_window: int, the short-term EMA window
        :param slow_window: int, the long-term EMA window
        :param signal_window: int, the signal line EMA window
        :return: tuple of pandas Series (MACD line, Signal line, MACD Histogram)
        """
        ema_fast = self.EMA(window=fast_window)
        ema_slow = self.EMA(window=slow_window)
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        
        return macd_line, signal_line, macd_histogram

# Example usage:
if __name__ == "__main__":
    # Sample data creation
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'Close': np.random.rand(100) * 100
    }
    df = pd.DataFrame(data)
    
    print(df.head())

    ti = TechnicalIndicators(df)
    
    # Calculate indicators
    print("SMA (10):\n", ti.SMA(10))
    print("EMA (10):\n", ti.EMA(10))
    print("RSI (14):\n", ti.RSI(14))
    macd_line, signal_line, macd_histogram = ti.MACD()
    print("MACD Line:\n", macd_line)
    print("Signal Line:\n", signal_line)
    print("MACD Histogram:\n", macd_histogram)

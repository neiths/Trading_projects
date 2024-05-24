import pandas as pd

class Indicators:
    def __init__(self, data_frame: pd.DataFrame) -> None:
        self.data_frame = data_frame
    
    def rsi(self, period: int = 14) -> None:
        close_delta = self.data_frame['Close'].diff()

        gain = close_delta.where(close_delta > 0, 0)
        loss = -close_delta.where(close_delta < 0, 0)

        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        self.data_frame['rsi'] = rsi
    
    def sma(self, period: int = 30) -> None:
        self.data_frame['sma'] = self.data_frame['Close'].rolling(window=period).mean()
    
    def ema(self, period: int = 30) -> None:
        self.data_frame['ema'] = self.data_frame['Close'].ewm(span=period, adjust=False).mean()
    
    def macd(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> None:
        self.data_frame['macd_fast'] = self.data_frame['Close'].ewm(span=fast_period, adjust=False).mean()
        self.data_frame['macd_slow'] = self.data_frame['Close'].ewm(span=slow_period, adjust=False).mean()
        self.data_frame['macd'] = self.data_frame['macd_fast'] - self.data_frame['macd_slow']
        self.data_frame['macd_signal'] = self.data_frame['macd'].ewm(span=signal_period, adjust=False).mean()
    
    def bollinger_bands(self, period: int = 20, std_dev: int = 2) -> None:
        self.data_frame['sma'] = self.data_frame['Close'].rolling(window=period).mean()
        self.data_frame['std'] = self.data_frame['Close'].rolling(window=period).std()

        self.data_frame['bollinger_upper'] = self.data_frame['sma'] + (self.data_frame['std'] * std_dev)
        self.data_frame['bollinger_lower'] = self.data_frame['sma'] - (self.data_frame['std'] * std_dev)



df = pd.read_csv('AAPL.csv')
indicators = Indicators(data_frame=df)

# Step 3: Apply the various indicators as needed

# Example: Calculate RSI
indicators.rsi(period=14)
print(indicators.data_frame.head())

# Example: Calculate SMA
indicators.sma(period=30)
print(indicators.data_frame.head())

# Example: Calculate EMA
indicators.ema(period=30)
print(indicators.data_frame.head())

# Example: Calculate MACD
indicators.macd(fast_period=12, slow_period=26)
print(indicators.data_frame.head())

# Example: Calculate Bollinger Bands
indicators.bollinger_bands(period=20)
print(indicators.data_frame.head())
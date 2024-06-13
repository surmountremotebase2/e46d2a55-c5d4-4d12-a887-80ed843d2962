from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Choosing '1day' to align with the daily SMA indicators
        return "1day"
    
    def run(self, data):
        # Retrieve OHLCV data for the asset
        ohlcv_data = data["ohlcv"]
        
        # Compute short-term and long-term SMAs
        short_sma = SMA(self.ticker, ohlcv_data, 20)
        long_sma = SMA(self.ticker, ohlcv_data, 50)
        
        allocation = 0
        
        # Check if both SMAs are calculable
        if short_sma is not None and long_sma is not None:
            # Identify the crossover event
            if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
                log(f"Going long on {self.ticker}, short-term SMA crossed above long-term SMA")
                allocation = 1  # Allocate 100% to buying
            elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
                log(f"Selling off or not holding {self.ticker}, short-term SMA crossed below long-term SMA")
                allocation = 0  # Sell or do not hold
        
        # Return the allocation as a TargetAllocation object
        return TargetAllocation({self.ticker: allocation})
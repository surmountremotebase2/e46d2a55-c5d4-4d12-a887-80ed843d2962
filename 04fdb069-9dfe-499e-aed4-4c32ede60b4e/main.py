from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # The tickers to track
        self.tickers = ["SPY"]
        
    @property
    def interval(self):
        # The interval for data collection. For this simple crossover, let's use daily data.
        return "1day"

    @property
    def assets(self):
        # The assets this strategy is concerned with.
        return self.tickers

    @property
    def data(self):
        # No additional data required beyond the default OHLCV.
        return []

    def run(self, data):
        # Retrieve the historical OHLCV data for the asset.
        spy_data = data["ohlcv"]
        
        # Ensure there's enough data to compute the SMAs
        if len(spy_data) >= 50:  # Using 50 as an example for the slow SMA period
            fast_sma = SMA("SPY", spy_data, 10)  # 10-period SMA as the fast moving average
            slow_sma = SMA("SPY", spy_data, 50)  # 50-period SMA as the slow moving average
            
            if fast_sma[-1] > slow_sma[-1] and fast_sma[-2] <= slow_sma[-2]:
                # Fast SMA crossed above Slow SMA, consider buying
                log("Fast SMA crossed above Slow SMA, buying SPY.")
                target_allocation = {"SPY": 1.0}  # Allocates 100% of portfolio to SPY
            elif fast_sma[-1] < slow_sma[-1] and fast_sma[-2] >= slow_sma[-2]:
                # Fast SMA crossed below Slow SMA, consider staying out
                log("Fast SMA crossed below Slow SMA, staying out of SPY.")
                target_allocation = {"SPY": 0}  # Allocates 0% of portfolio to SPY
            else:
                # No crossover event, maintain current allocation
                log("No SMA crossover, maintaining current allocation.")
                target_allocation = {}  # Returns an empty dict, indicating no change
        else:
            # Not enough data to compute SMAs
            log("Insufficient data to compute SMAs, no action taken.")
            target_allocation = {}  # Returns an empty dict, indicating no change
        
        return TargetAccounting(target_allocation)
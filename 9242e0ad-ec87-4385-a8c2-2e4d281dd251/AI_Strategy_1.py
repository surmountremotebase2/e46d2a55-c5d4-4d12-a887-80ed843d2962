from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Specifying the asset to trade

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Using daily data for the MACD calculation

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate MACD using the default parameters
            macd = MACD(ticker=ticker, data=data["ohlcv"], fast=12, slow=26)
            if macd is not None:
                # Compare MACD to its signal line
                macd_line = macd["MACD"]
                signal_line = macd["signal"]
                
                # Ensure we have enough data points to make a decision
                if len(macd_line) > 1 and len(signal_line) > 1:
                    current_macd = macd_line[-1]
                    previous_macd = macd_line[-2]
                    current_signal = signal_line[-1]
                    previous_signal = signal_line[-2]
                    
                    # Logic to determine if we should buy/sell based on MACD crossover
                    if current_macd > current_signal and previous_macd <= previous_signal:
                        log(f"MACD crossover above signal line for {ticker}. Buying signal.")
                        allocation_dict[ticker] = 1.0  # Fully invest in this asset
                    elif current_macd < current_signal and previous_macd >= previous_signal:
                        log(f"MACD crossover below signal line for {ticker}. Selling signal.")
                        allocation_dict[ticker] = 0.0  # Exit this asset
                    else:
                        log(f"No MACD crossover signal for {ticker}. Holding position.")
                        # If we're already invested, maintain the current allocation
                        # This part depends on your risk management criteria, and 
                        # you might want to adjust the logic to suit your needs
                        allocation_dict[ticker] = allocation_dict.get(ticker, 0)
                else:
                    log("Not enough data for MACD calculation.")
            else:
                log(f"MACD calculation failed for {ticker}.")
                
        return TargetAllocation(allocation_dict)
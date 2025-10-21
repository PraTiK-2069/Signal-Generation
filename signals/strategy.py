import numpy as np
from typing import Sequence
import yfinance as yf

class BreakoutSignal:
    def __init__(self, lookback: int):  
        self.lookback = lookback
    
    def generate(self, prices: Sequence[float]) -> np.ndarray:
        prices = np.array(prices)
        signals = np.zeros_like(prices, dtype=int)

        for i in range(self.lookback, len(prices)):
            window = prices[i-self.lookback:i]
            signals[i] = np.where(prices[i] > window.max(), 1, np.where(prices[i] < window.min(), -1, 0))
        return signals
    
class MovingAverageCrossOver:
    def __init__(self, short: int, long: int): 
        self.short = short
        self.long = long
    
    def moving_average(self, prices: Sequence[float], window: int) -> np.ndarray:
        prices = np.array(prices, dtype=float)
        ma = np.zeros_like(prices, dtype=float)
        for i in range(len(prices)):
            if i + 1 < window:
                ma[i] = 0 
            else:
                ma[i] = np.mean(prices[i+1-window:i+1])
        return ma

    def generate_ma_signals(self, prices: Sequence[float]) -> np.ndarray:
        short_ma = self.moving_average(prices, self.short)
        long_ma = self.moving_average(prices, self.long)
        signals = np.where(short_ma > long_ma, 1,
                           np.where(short_ma < long_ma, -1, 0))
        return signals
    
class SignalCombiner:
    def __init__(self): 
        return
    
    def combine(self, signal1, signal2):
        final_signal = []
        for sig1, sig2 in zip(signal1, signal2):
            final_signal.append((sig1 + sig2) // 2)
        return np.array(final_signal) 


ticker_symbol = "META"
prices = list(yf.download(tickers=ticker_symbol, start="2020-01-01", end="2025-10-21")['Close'][ticker_symbol])

lookback = 2
breakout = BreakoutSignal(lookback)
signals_breakout = breakout.generate(prices)
print("signals_breakout: ", signals_breakout.tolist())

short_window = 2
long_window = 3
mac = MovingAverageCrossOver(short_window, long_window)
signals_mac = mac.generate_ma_signals(prices)
print("signals_mac     : ", signals_mac.tolist())

signal_combiner = SignalCombiner()
final_signal = signal_combiner.combine(signals_breakout, signals_mac)
print("final signal    : ", final_signal)

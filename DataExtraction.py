from TradingView import TradingViewData, Interval
import pandas as pd
from typing import List
import os


def create_csv(folder_path: str, symbol: str, request: TradingViewData):

    df: pd.DataFrame = request.get_hist(
        symbol=symbol, exchange="CRYPTO", interval=Interval.daily, n_bars=4 * 365
    )

    file_path = os.path.join(folder_path, f"{symbol}.csv")
    df.to_csv(file_path)


def main():
    folder_path = "data"
    request = TradingViewData()

    cryptos: List[str] = [
        "BTCUSD",
        "ETHUSD",
        "XRPUSD",
        "SOLUSD",
        "DOGEUSD",
        "ADAUSD",
        "SHIBUSD",
        "DOTUSD",
        "AAVEUSD",
        "XLMUSD",
    ]

    for crypto in cryptos:
        create_csv(folder_path, crypto, request)


if __name__ == "__main__":
    main()

from TradingView import TradingViewData, Interval
import pandas as pd
from typing import List
import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


def check_nan(df: pd.DataFrame, symbol: str, min_date, max_date):
    """Verifica si el DataFrame tiene valores NaN y si faltan fechas en el rango dado."""

    date_sequence = pd.date_range(min_date, max_date, freq="D").date

    has_nan = df.isna().sum().sum() > 0
    missing_dates = [
        date for date in date_sequence if date not in df["datetime"].values
    ]

    if has_nan:
        print(
            f"{Fore.RED}❌ The dataframe of coin {symbol} has missing values.{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.GREEN}✅ The dataframe of coin {symbol} does NOT have missing values.{Style.RESET_ALL}"
        )

        # Comprobación de fechas faltantes
    if len(missing_dates) == 0:
        print(
            f"{Fore.GREEN}✅ The dates column of coin {symbol} is correct.{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}❌ The dates column of coin {symbol} is missing some dates: {missing_dates}{Style.RESET_ALL}"
        )


def create_csv(folder_path: str, symbol: str, request: TradingViewData):
    """Genera un archivo CSV con los datos de la criptomoneda y verifica su integridad."""

    df: pd.DataFrame = request.get_hist(
        symbol=symbol, exchange="CRYPTO", interval=Interval.daily, n_bars=4 * 365
    ).reset_index()

    file_path = os.path.join(folder_path, f"{symbol}.csv")

    df["datetime"] = pd.to_datetime(df["datetime"]).dt.date
    df.drop(columns="symbol").to_csv(file_path, index=False)

    check_nan(df, symbol, df["datetime"].min(), df["datetime"].max())

    # Comprobación de almacenamiento exitoso
    if os.path.exists(file_path):
        print(
            f"{Fore.GREEN}✅ CSV for {symbol} saved successfully at {file_path}.{Style.RESET_ALL}"
        )
    else:
        print(f"{Fore.RED}❌ Failed to save CSV for {symbol}.{Style.RESET_ALL}")


def main():
    """Ejecuta el proceso de descarga y validación para varias criptomonedas."""

    folder_path = "data"

    os.makedirs(folder_path, exist_ok=True)

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
        print("*" * 10)


if __name__ == "__main__":
    main()

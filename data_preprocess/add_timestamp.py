# add_timestamp.py

import pandas as pd

def add_timestamp(file, file_timestamp):
    rows_data = 65

    df = pd.read_csv(file)
    df_timestamp = pd.read_csv(file_timestamp, skiprows=rows_data)

    timestamp = df_timestamp["Time(sec)"]
    df.insert(0, "timestamp", timestamp)

    df.to_csv("jointinfo_timestamp.csv")

if __name__=="__main__":
    file_pandas = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200514/jointinfo.csv"
    timestamp_pandas = "/Users/younghoonji/Desktop/2020_Spring/Project/golf_db/gears_data/200514/CsvExport.csv"
    add_timestamp(file_pandas, timestamp_pandas)
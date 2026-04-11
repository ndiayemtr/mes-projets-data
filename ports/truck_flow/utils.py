def add_time_features(df):
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.dayofweek
    return df


def create_lags(df):
    df["lag_1"] = df["truck_count"].shift(1)
    df["lag_2"] = df["truck_count"].shift(2)
    return df
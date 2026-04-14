import pandas as pd

def create_features(df):
    """
    Ajoute les features avancées utilisées par le modèle
    """

    df = df.copy()

    # Features temporelles
    df["vibration_diff"] = df["vibration"].diff()
    df["vibration_mean"] = df["vibration"].rolling(5).mean()
    df["vibration_std"] = df["vibration"].rolling(5).std()

    # Feature combinée (très importante)
    df["stress_index"] = df["temperature"] * df["vibration"]

    return df


def prepare_input(temp, vib, power, load, wind, hours):
    """
    Simule un historique pour calculer rolling features
    """

    df_input = pd.DataFrame({
        "temperature": [70, 72, 75, 80, temp],
        "vibration": [5, 5.5, 6, 7, vib],
        "power_consumption": [200, 210, 220, 250, power],
        "load_weight": [30, 32, 28, 35, load],
        "wind_speed": [10, 12, 8, 15, wind],
        "operating_hours": [5, 6, 7, 8, hours]
    })

    df_input = create_features(df_input)

    # garder dernière ligne
    df_input = df_input.tail(1)

    return df_input
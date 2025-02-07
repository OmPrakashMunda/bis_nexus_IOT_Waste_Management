def preprocess_data(df):
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month

    features = [
        'bin_id', 'hour', 'day_of_week', 'month',
        'temperature', 'humidity', 'location_lat', 'location_long'
    ]
    return features
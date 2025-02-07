import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import preprocess_data

class WasteManagementAI:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.fill_predictor = RandomForestRegressor(n_estimators=100)
        self.type_classifier = RandomForestClassifier(n_estimators=100)
        self.threshold = 80  # Fill level threshold for collection

    def prepare_features(self):
        return preprocess_data(self.data)

    def train_models(self):
        features = self.prepare_features()
        X = self.data[features]
        y_fill = self.data['fill_level']
        y_type = self.data['waste_type']

        X_train, X_test, y_fill_train, y_fill_test, y_type_train, y_type_test = train_test_split(
            X, y_fill, y_type, test_size=0.2
        )

        self.fill_predictor.fit(X_train, y_fill_train)
        self.type_classifier.fit(X_train, y_type_train)

        metrics = {
            'fill_rmse': np.sqrt(mean_squared_error(y_fill_test, 
                               self.fill_predictor.predict(X_test))),
            'type_accuracy': accuracy_score(y_type_test, 
                                         self.type_classifier.predict(X_test))
        }
        return metrics

    def predict_collections(self):
        features = self.prepare_features()
        predictions = self.fill_predictor.predict(self.data[features])
        return self.data[predictions > self.threshold]['bin_id'].unique()

    def optimize_route(self, bins):
        bin_data = self.data[self.data['bin_id'].isin(bins)][
            ['bin_id', 'location_lat', 'location_long']
        ].drop_duplicates()
        
        route = []
        current = bin_data.iloc[0]
        remaining = bin_data.iloc[1:].copy()

        while len(remaining) > 0:
            distances = np.sqrt(
                (remaining['location_lat'] - current['location_lat'])**2 +
                (remaining['location_long'] - current['location_long'])**2
            )
            next_bin = remaining.iloc[distances.argmin()]
            route.append(next_bin['bin_id'])
            current = next_bin
            remaining = remaining[remaining['bin_id'] != next_bin['bin_id']]

        return route
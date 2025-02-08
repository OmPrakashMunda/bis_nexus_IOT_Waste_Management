# ai/model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import List, Tuple

class WasteManagementAI:
    def __init__(self, data_path: str):
        """Initialize the AI model with data path."""
        self.data_path = data_path
        self.fill_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.data = None
        self.is_trained = False
        self._load_data()
        
    def _load_data(self) -> None:
        """Load and preprocess the data."""
        try:
            self.data = pd.read_csv(self.data_path)
            # Add dummy data if file is empty or doesn't exist
            if self.data.empty:
                self._create_dummy_data()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self._create_dummy_data()

    def _create_dummy_data(self) -> None:
        """Create dummy data for testing."""
        np.random.seed(42)
        n_samples = 1000
        
        self.data = pd.DataFrame({
            'bin_id': range(1, 21) * (n_samples // 20),
            'timestamp': pd.date_range(start='2024-01-01', periods=n_samples, freq='H'),
            'fill_level': np.random.uniform(0, 100, n_samples),
            'temperature': np.random.normal(25, 5, n_samples),
            'humidity': np.random.uniform(30, 80, n_samples),
            'waste_type': np.random.choice(['organic', 'recyclable', 'general'], n_samples),
            'collection_frequency': np.random.uniform(1, 5, n_samples)
        })

    def train_models(self) -> dict:
        """Train the AI models and return metrics."""
        # Prepare features
        features = ['temperature', 'humidity', 'collection_frequency']
        target = 'fill_level'
        
        # Handle missing values
        self.data = self.data.dropna(subset=features + [target])
        
        # Split data
        X = self.data[features]
        y = self.data[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.fill_predictor.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Calculate metrics
        train_score = self.fill_predictor.score(X_train_scaled, y_train)
        test_score = self.fill_predictor.score(X_test_scaled, y_test)
        
        return {
            'train_score': train_score,
            'test_score': test_score
        }

    def predict_collections(self) -> np.ndarray:
        """Predict which bins need collection."""
        if not self.is_trained:
            self.train_models()
            
        features = ['temperature', 'humidity', 'collection_frequency']
        
        # Get latest data for each bin
        latest_data = self.data.sort_values('timestamp').groupby('bin_id').last()
        
        # Make predictions
        X = self.scaler.transform(latest_data[features])
        predictions = self.fill_predictor.predict(X)
        
        # Get bins that need collection (fill level > 75%)
        bins_to_collect = latest_data.index[predictions > 75].values
        
        return bins_to_collect

    def optimize_route(self, bins: np.ndarray) -> List[int]:
        """Optimize the collection route for given bins."""
        if len(bins) == 0:
            return []
            
        # Simple route optimization (can be enhanced with actual routing algorithms)
        # Currently just sorts bins by predicted fill level in descending order
        latest_data = self.data.sort_values('timestamp').groupby('bin_id').last()
        bins_data = latest_data.loc[bins]
        optimized_route = bins_data.sort_values('fill_level', ascending=False).index.tolist()
        
        return optimized_route

# Main execution for testing
if __name__ == "__main__":
    ai = WasteManagementAI("data/waste_data.csv")
    metrics = ai.train_models()
    print("Training metrics:", metrics)
    
    bins_to_collect = ai.predict_collections()
    print("Bins that need collection:", bins_to_collect)
    
    optimized_route = ai.optimize_route(bins_to_collect)
    print("Optimized route:", optimized_route)
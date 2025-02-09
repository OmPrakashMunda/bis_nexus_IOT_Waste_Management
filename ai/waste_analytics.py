import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import joblib
import os

class WasteAnalytics:
    def __init__(self, data_path="../data/waste_management_data.csv"):
        """Initialize the analytics module with data path."""
        self.data_path = data_path
        self.df = None
        self.model = None
        self.load_data()
        
    def load_data(self):
        """Load and preprocess the waste management data."""
        self.df = pd.read_csv(self.data_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
    def get_current_status(self):
        """Get current status of all bins."""
        latest_records = self.df.sort_values('timestamp').groupby('bin_id').last()
        critical_bins = latest_records[latest_records['fill_level'] > 80]
        
        return {
            'total_bins': len(latest_records),
            'critical_bins': len(critical_bins),
            'avg_fill_level': round(latest_records['fill_level'].mean(), 2),
            'critical_locations': critical_bins['location'].tolist()
        }
    
    def get_location_analytics(self):
        """Analyze waste patterns by location."""
        location_stats = self.df.groupby('location').agg({
            'fill_level': 'mean',
            'fill_rate': 'mean',
            'bin_id': 'nunique'
        }).round(2)
        
        return location_stats.to_dict(orient='index')
    
    def get_waste_type_distribution(self):
        """Analyze waste type distribution."""
        waste_dist = self.df.groupby('waste_type').size()
        total = len(self.df)
        
        return {
            waste_type: {
                'count': int(count),
                'percentage': round((count/total) * 100, 2)
            }
            for waste_type, count in waste_dist.items()
        }
    
    def predict_collection_schedule(self):
        """Predict optimal collection schedule based on fill rates."""
        latest_records = self.df.sort_values('timestamp').groupby('bin_id').last()
        
        predictions = {}
        for bin_id, row in latest_records.iterrows():
            current_fill = row['fill_level']
            fill_rate = row['fill_rate']
            
            if fill_rate > 0:
                hours_until_full = (100 - current_fill) / fill_rate
                predicted_full = datetime.now() + timedelta(hours=hours_until_full)
                
                predictions[bin_id] = {
                    'current_fill': round(current_fill, 2),
                    'fill_rate': round(fill_rate, 2),
                    'hours_until_full': round(hours_until_full, 2),
                    'predicted_full_time': predicted_full.strftime('%Y-%m-%d %H:%M:%S'),
                    'location': row['location'],
                    'priority': 'High' if hours_until_full < 24 else 'Medium' if hours_until_full < 48 else 'Low'
                }
        
        return predictions
    
    def get_historical_trends(self, days=7):
        """Analyze historical trends in waste generation."""
        self.df['date'] = self.df['timestamp'].dt.date
        recent_data = self.df[self.df['timestamp'] >= (datetime.now() - timedelta(days=days))]
        
        daily_trends = recent_data.groupby(['date', 'waste_type'])['fill_level'].mean().round(2)
        return daily_trends.to_dict()
    
    def identify_optimal_bin_locations(self):
        """Use K-means clustering to suggest optimal bin locations based on fill patterns."""
        features = ['fill_rate', 'fill_level']
        X = self.df[features]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=3, random_state=42)
        self.df['usage_cluster'] = kmeans.fit_predict(X_scaled)
        
        cluster_analysis = self.df.groupby(['location', 'usage_cluster']).size().unstack(fill_value=0)
        dominant_clusters = cluster_analysis.idxmax(axis=1)
        
        recommendations = {
            'High Traffic': dominant_clusters[dominant_clusters == 2].index.tolist(),
            'Medium Traffic': dominant_clusters[dominant_clusters == 1].index.tolist(),
            'Low Traffic': dominant_clusters[dominant_clusters == 0].index.tolist()
        }
        
        return recommendations
    
    def get_efficiency_metrics(self):
        """Calculate waste management efficiency metrics."""
        collection_data = self.df[self.df['fill_level'] < 20].groupby('bin_id').size()
        overflow_data = self.df[self.df['fill_level'] > 90].groupby('bin_id').size()
        
        metrics = {
            'collection_efficiency': {
                'total_collections': int(collection_data.sum()),
                'avg_collections_per_bin': round(collection_data.mean(), 2)
            },
            'overflow_incidents': {
                'total_overflows': int(overflow_data.sum()),
                'bins_with_overflow': len(overflow_data)
            }
        }
        
        return metrics

if __name__ == "__main__":
    analytics = WasteAnalytics()
    print("Current Status:", analytics.get_current_status())
    print("\nLocation Analytics:", analytics.get_location_analytics())
    print("\nWaste Distribution:", analytics.get_waste_type_distribution())
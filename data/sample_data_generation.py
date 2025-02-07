from datetime import datetime, timedelta
import pandas as pd
import random

BASE_LAT = 20.289594
BASE_LONG = 85.835212

num_records = 1000
bin_ids = range(1, 21)
waste_types = ['Organic', 'Recyclable', 'General', 'Hazardous']

data = {
    'timestamp': [],
    'bin_id': [],
    'fill_level': [],
    'waste_type': [],
    'temperature': [],
    'humidity': [],
    'weight': [],
    'location_lat': [],
    'location_long': [],
    'collection_frequency': [],
    'fill_rate': []
}

start_date = datetime.now() - timedelta(days=365)
for _ in range(num_records):
    lat = BASE_LAT + random.uniform(-0.05, 0.05)
    long = BASE_LONG + random.uniform(-0.05, 0.05)
    
    data['timestamp'].append(start_date + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23)))
    data['bin_id'].append(random.choice(bin_ids))
    data['fill_level'].append(round(random.uniform(0, 100), 2))
    data['waste_type'].append(random.choice(waste_types))
    data['temperature'].append(round(random.uniform(25, 40), 2))
    data['humidity'].append(round(random.uniform(60, 90), 2))
    data['weight'].append(round(random.uniform(0, 50), 2))
    data['location_lat'].append(round(lat, 6))
    data['location_long'].append(round(long, 6))
    data['collection_frequency'].append(random.randint(1, 7))
    data['fill_rate'].append(round(random.uniform(0.1, 2.0), 2))

df = pd.DataFrame(data)
df = df.sort_values('timestamp')
df.to_csv('bhubaneswar_waste_data.csv', index=False)

print(df.head())
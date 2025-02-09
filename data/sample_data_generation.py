import random
from datetime import datetime, timedelta
import csv
locations = [
    "Campus 1", "Campus 3", "Campus 4", "Campus 6", "Campus 12", "Campus 13",
    "Central Library", "KP 1", "KP 5", "KP 6", "KP 7",
    "KP 12", "KP 22", "QC 1", "QC 2", "QC 3",
    "QC 4", "QC 5", "QC 6", "QC 7", "QC 8",
    "QC 9", "QC 10", "QC 11", "QC 12"
]

waste_types = ["Organic", "Recyclable", "Hazardous", "E-waste", "Mixed"]
collection_frequencies = ["Daily", "Twice Daily", "Weekly", "Twice Weekly"]

bin_ids = []
for loc in locations:
    num_bins = random.randint(2, 5) 
    for i in range(num_bins):
        bin_ids.append(f"{loc.replace(' ', '')}_BIN_{i+1}")

def generate_waste_data(num_records):
    data = []
    current_time = datetime.now()
    
    bin_fill_levels = {bin_id: random.uniform(0, 20) for bin_id in bin_ids}
    
    for _ in range(num_records):
        bin_id = random.choice(bin_ids)
        location = bin_id.split('_BIN_')[0]
        for char in ['Campus', 'KPHostel', 'QCHostel']:
            location = location.replace(char, char + ' ')
        
        current_fill = bin_fill_levels[bin_id]
        fill_rate = random.uniform(0.5, 2.5)  
        hours_passed = random.randint(1, 4)
        new_fill = min(100, current_fill + (fill_rate * hours_passed))
        bin_fill_levels[bin_id] = new_fill
        
        if new_fill > 80:
            if random.random() < 0.7:
                bin_fill_levels[bin_id] = random.uniform(0, 20)
                new_fill = bin_fill_levels[bin_id]
        
        record = {
            'timestamp': (current_time + timedelta(hours=hours_passed)).strftime('%Y-%m-%d %H:%M:%S'),
            'bin_id': bin_id,
            'fill_level': round(new_fill, 2),
            'waste_type': random.choice(waste_types),
            'location': location,
            'collection_frequency': random.choice(collection_frequencies),
            'fill_rate': round(fill_rate, 2)
        }
        
        data.append(record)
        current_time += timedelta(hours=hours_passed)
    
    return data

waste_data = generate_waste_data(1000)

csv_file = 'waste_management_data.csv'
with open(csv_file, 'w', newline='') as file:
    fieldnames = ['timestamp', 'bin_id', 'fill_level', 'waste_type', 'location', 
                 'collection_frequency', 'fill_rate']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(waste_data)

print(f"Generated {len(waste_data)} records and saved to {csv_file}")
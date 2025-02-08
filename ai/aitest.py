import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump

# Generate Sample Data (You should use real sensor data)
data = {
    "day": np.arange(1, 31),  # Days (e.g., 30 days of data)
    "waste_fill_level": np.random.randint(10, 100, 30)  # Random fill levels (10% to 100%)
}

df = pd.DataFrame(data)

# Target Variable: Predict the fill level for the next day
X = df[["day"]]
y = df["waste_fill_level"]

# Split the dataset for training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
dump(model, "waste_prediction_model.pkl")

print("Model trained and saved!")

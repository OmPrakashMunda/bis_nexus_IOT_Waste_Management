class Config:
    DATABASE_URL = "sqlite:///waste_management.db"
    AI_MODEL_PATH = "../data/bhubaneswar_waste_data.csv"
    UPDATE_INTERVAL = 300  # seconds
    COLLECTION_THRESHOLD = 80  # percentage
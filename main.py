import uvicorn
from fastapi import FastAPI, HTTPException
from backend.database import Database
from ai.model import WasteManagementAI
import unittest
import numpy as np
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Waste Management AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = Database()
ai_model = WasteManagementAI('data/bhubaneswar_waste_data.csv')
metrics = ai_model.train_models()

class BinData(BaseModel):
   bin_id: int
   fill_level: float
   temperature: float
   humidity: float
   location_lat: float
   location_long: float
   waste_type: str
   timestamp: Optional[datetime] = None

# AI Predictions
@app.get("/predictions")
async def get_predictions():
   bins = ai_model.predict_collections()
   route = ai_model.optimize_route(bins)
   return {
       "bins_to_collect": bins.tolist(),
       "optimized_route": route
   }

# Update Bin Data
@app.post("/update")
async def update_bin_data(data: BinData):
   try:
       db.insert_bin_data(data.dict())
       ai_model.train_models()
       return {"status": "success", "message": "Data updated successfully"}
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

# Get Statistics
@app.get("/stats")
async def get_stats():
   return db.get_statistics()

# Get Bin Details
@app.get("/bin/{bin_id}")
async def get_bin_details(bin_id: int):
   try:
       bin_data = db.get_bin_data(bin_id)
       return {"bin_id": bin_id, "data": bin_data}
   except Exception as e:
       raise HTTPException(status_code=404, detail=f"Bin {bin_id} not found")

# Get All Bins
@app.get("/bins")
async def get_all_bins():
   bins = db.get_all_bins()
   return {"bins": bins}

# Get Optimized Route
@app.get("/route")
async def get_route():
   bins = ai_model.predict_collections()
   route = ai_model.optimize_route(bins)
   return {"route": route}

# Get Waste Types Distribution
@app.get("/waste-types")
async def get_waste_distribution():
   distribution = db.get_waste_distribution()
   return {"distribution": distribution}

# Health Check
@app.get("/health")
async def health_check():
   return {"status": "healthy", "timestamp": datetime.now()}

class TestWasteManagementAI(unittest.TestCase):
   def setUp(self):
       self.ai = WasteManagementAI('data/bhubaneswar_waste_data.csv')

   def test_predict_collections(self):
       bins = self.ai.predict_collections()
       self.assertIsInstance(bins, np.ndarray)
       self.assertTrue(len(bins) > 0)

   def test_optimize_route(self):
       bins = self.ai.predict_collections()
       route = self.ai.optimize_route(bins)
       self.assertEqual(len(route), len(bins))

if __name__ == "__main__":
   # Run tests
   suite = unittest.TestLoader().loadTestsFromTestCase(TestWasteManagementAI)
   unittest.TextTestRunner(verbosity=2).run(suite)
   
   # Start server
   uvicorn.run(app, host="127.0.0.1", port=8000)
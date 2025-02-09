from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai.waste_analytics import WasteAnalytics
from typing import Dict, List, Any
import uvicorn
app = FastAPI(title="Smart Waste Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
analytics = WasteAnalytics(data_path="data/waste_management_data.csv")

@app.get("/")
async def root():
    return {"message": "Smart Waste Management API is running"}

@app.get("/api/current-status")
async def get_current_status() -> Dict[str, Any]:
    """Get current status of all waste bins."""
    try:
        return analytics.get_current_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/location-analytics")
async def get_location_analytics() -> Dict[str, Any]:
    """Get analytics breakdown by location."""
    try:
        return analytics.get_location_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/waste-distribution")
async def get_waste_distribution() -> Dict[str, Any]:
    """Get waste type distribution analysis."""
    try:
        return analytics.get_waste_type_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/collection-schedule")
async def get_collection_schedule() -> Dict[str, Any]:
    """Get predicted collection schedule."""
    try:
        return analytics.predict_collection_schedule()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/historical-trends")
async def get_historical_trends(days: int = 7) -> Dict[str, Any]:
    """Get historical waste generation trends."""
    try:
        return analytics.get_historical_trends(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimal-locations")
async def get_optimal_locations() -> Dict[str, List[str]]:
    """Get optimal bin location recommendations."""
    try:
        return analytics.identify_optimal_bin_locations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/efficiency-metrics")
async def get_efficiency_metrics() -> Dict[str, Any]:
    """Get waste management efficiency metrics."""
    try:
        return analytics.get_efficiency_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
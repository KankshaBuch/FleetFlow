from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Vehicle, Driver
from datetime import date

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "FleetFlow Running"}

# Add Vehicle
@app.post("/add_vehicle")
def add_vehicle(name: str, plate: str, max_weight: float, buy_price: float, db: Session = Depends(get_db)):
    vehicle = Vehicle(
        name=name,
        plate=plate,
        max_weight=max_weight,
        buy_price=buy_price
    )
    db.add(vehicle)
    db.commit()
    return {"message": "Vehicle added"}

# Add Driver
@app.post("/add_driver")
def add_driver(name: str, expiry_year: int, db: Session = Depends(get_db)):
    driver = Driver(
        name=name,
        license_expiry=date(expiry_year, 1, 1)
    )
    db.add(driver)
    db.commit()
    return {"message": "Driver added"}

# Start Trip
@app.post("/start_trip")
def start_trip(vehicle_id: int, driver_id: int, cargo_weight: float, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).get(vehicle_id)
    driver = db.query(Driver).get(driver_id)

    if not vehicle or not driver:
        raise HTTPException(status_code=404, detail="Vehicle or Driver not found")

    if vehicle.status != "Available":
        raise HTTPException(status_code=400, detail="Vehicle not available")

    if driver.status != "On Duty":
        raise HTTPException(status_code=400, detail="Driver not on duty")

    if cargo_weight > vehicle.max_weight:
        raise HTTPException(status_code=400, detail="Cargo exceeds capacity")

    if driver.license_expiry.year < date.today().year:
        raise HTTPException(status_code=400, detail="License expired")

    vehicle.status = "On Trip"
    driver.status = "On Trip"
    db.commit()

    return {"message": "Trip started successfully"}

# Maintenance
@app.post("/maintenance")
def maintenance(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).get(vehicle_id)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle.status = "In Shop"
    db.commit()

    return {"message": "Vehicle moved to maintenance"}

@app.get("/drivers")
def list_drivers(db: Session = Depends(get_db)):
    drivers = db.query(Driver).all()
    return drivers

@app.get("/vehicles")
def list_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total = db.query(Vehicle).count()
    active = db.query(Vehicle).filter(Vehicle.status == "On Trip").count()
    in_shop = db.query(Vehicle).filter(Vehicle.status == "In Shop").count()

    utilization = (active / total) * 100 if total else 0

    return {
        "total_vehicles": total,
        "active_fleet": active,
        "maintenance": in_shop,
        "utilization_rate": utilization
    }

@app.post("/complete_trip")
def complete_trip(vehicle_id: int, driver_id: int, final_odometer: float, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).get(vehicle_id)
    driver = db.query(Driver).get(driver_id)

    if not vehicle or not driver:
        raise HTTPException(status_code=404, detail="Vehicle or Driver not found")

    vehicle.status = "Available"
    driver.status = "On Duty"
    vehicle.odometer = final_odometer

    db.commit()

    return {"message": "Trip completed successfully"}

from models import FuelLog

@app.post("/add_fuel")
def add_fuel(vehicle_id: int, liters: float, cost: float, db: Session = Depends(get_db)):
    fuel = FuelLog(vehicle_id=vehicle_id, liters=liters, cost=cost)
    db.add(fuel)
    db.commit()
    return {"message": "Fuel logged"}

from sqlalchemy import func

@app.get("/analytics/{vehicle_id}")
def analytics(vehicle_id: int, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).get(vehicle_id)

    total_fuel_cost = db.query(func.sum(FuelLog.cost))\
        .filter(FuelLog.vehicle_id == vehicle_id).scalar() or 0

    total_liters = db.query(func.sum(FuelLog.liters))\
        .filter(FuelLog.vehicle_id == vehicle_id).scalar() or 0

    roi = 0
    if vehicle.buy_price:
        roi = ((10000 - total_fuel_cost) / vehicle.buy_price) * 100  # Demo revenue = 10000

    efficiency = vehicle.odometer / total_liters if total_liters else 0

    return {
        "fuel_cost": total_fuel_cost,
        "efficiency_km_per_l": efficiency,
        "roi_percent": roi
    }
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import HTTPException

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)
    db.commit()
    return {"message": "Deleted successfully"}
from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    plate = Column(String, unique=True)
    max_weight = Column(Float)
    buy_price = Column(Float)
    odometer = Column(Float, default=0)
    status = Column(String, default="Available")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    license_expiry = Column(Date)
    status = Column(String, default="On Duty")
    safety_score = Column(Integer, default=100)

class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer)
    liters = Column(Float)
    cost = Column(Float)

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WaterFootprint(Base):
    __tablename__ = 'water_footprint'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, unique=True, nullable=False, index=True)
    green_wf = Column(Float, nullable=False)
    blue_wf = Column(Float, nullable=False)
    grey_wf = Column(Float, nullable=False)
    unit = Column(String, default="litres/kg")

class ComparisonReference(Base):
    __tablename__ = 'comparison_reference'

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_name = Column(String, unique=True, nullable=False)
    litres = Column(Float, nullable=False)

class AltSuggestions(Base):
    __tablename__ = 'alt_suggestions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    high_footprint_item = Column(String, unique=True, nullable=False)
    suggested_alt = Column(String, nullable=False)
    reason = Column(String, nullable=False)

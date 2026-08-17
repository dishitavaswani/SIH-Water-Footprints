try:
    from sqlalchemy import Column, Integer, String, Float, Text
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class WaterFootprint(Base):
        """
        SQLAlchemy Model for agricultural water footprint data.
        Table: water_footprint
        """
        __tablename__ = 'water_footprint'

        id = Column(Integer, primary_key=True, autoincrement=True)
        item_name = Column(String, unique=True, nullable=False, index=True)
        green_wf = Column(Float, nullable=False)
        blue_wf = Column(Float, nullable=False)
        grey_wf = Column(Float, nullable=False)
        unit = Column(String, default="litres/kg", nullable=False)

    class ComparisonReference(Base):
        """
        Benchmark household objects for relatable water volume comparisons.
        Table: comparison_reference
        """
        __tablename__ = 'comparison_reference'

        id = Column(Integer, primary_key=True, autoincrement=True)
        object_name = Column(String, unique=True, nullable=False)
        litres = Column(Float, nullable=False)

    class AltSuggestions(Base):
        """
        Actionable eco-friendly alternative food suggestions.
        Table: alt_suggestions
        """
        __tablename__ = 'alt_suggestions'

        id = Column(Integer, primary_key=True, autoincrement=True)
        high_footprint_item = Column(String, unique=True, nullable=False, index=True)
        suggested_alt = Column(String, nullable=False)
        reason = Column(Text, nullable=False)

    HAS_SQLALCHEMY = True

except ImportError:
    HAS_SQLALCHEMY = False
    Base = object

    class WaterFootprint:
        __tablename__ = 'water_footprint'

    class ComparisonReference:
        __tablename__ = 'comparison_reference'

    class AltSuggestions:
        __tablename__ = 'alt_suggestions'

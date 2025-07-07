from sqlalchemy import Column, Integer, String
from .database import Base


class USCrudeOilImport(Base):
    __tablename__ = 'us_crude_oil_imports'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    originName = Column(String)
    originTypeName = Column(String)
    destinationName = Column(String)
    destinationTypeName = Column(String)
    gradeName = Column(String)
    quantity = Column(Integer)

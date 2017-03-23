#!/usr/bin/env python3

""" Mapping of class """

from sqlalchemy import Column, Float, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Materials(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    material_type = Column(String)
    price = Column(Integer)
    classlvl = Column(Integer)
    owned = Column(String)

    def __init__(self, material_type, price, classlvl):
        """ init method """
        self.material_type = material_type
        self.price = price
        self.classlvl = classlvl

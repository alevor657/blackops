#!/usr/bin/env python3

""" Mapping of class """

from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workers(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    occupation = Column(String)
    classlvl = Column(Integer)

    def __init__(self, name, occupation, classlvl):
        """ init method """
        self.name = name
        self.occupation = occupation
        self.classlvl = classlvl

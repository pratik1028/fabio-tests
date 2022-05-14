from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Column, Integer, VARCHAR, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base(metadata=MetaData(schema='wikipedia'))


class Continent(Base):
    __tablename__ = "continent"
    continent_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    population = Column(BigInteger)
    area = Column(VARCHAR)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    countries = relationship('Country',
                             back_populates='continent',
                             cascade="all, delete",
                             passive_deletes=True
                             )


class Country(Base):
    __tablename__ = "country"
    country_id = Column(Integer, primary_key=True)
    continent_id = Column(Integer, ForeignKey("continent.continent_id", ondelete="CASCADE"))
    name = Column(VARCHAR)
    population = Column(BigInteger)
    area = Column(VARCHAR)
    hospitals = Column(Integer, default=0)
    national_parks = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    continent = relationship('Continent', back_populates='countries')
    cities = relationship('City',
                          back_populates='country',
                          cascade="all, delete",
                          passive_deletes=True
                          )


class City(Base):
    __tablename__ = "city"
    city_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country.country_id", ondelete="CASCADE"))
    name = Column(VARCHAR)
    population = Column(BigInteger)
    area = Column(VARCHAR)
    roads = Column(Integer, default=0)
    trees = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    country = relationship('Country', back_populates='cities')

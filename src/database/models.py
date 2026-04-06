from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



DB_PATH = "/Users/nikita/Desktop/frontend road/projects/University bot/database.db"

base_engine = create_engine(f'sqlite:////{DB_PATH}', echo=True) # Оставим echo=True пока проверяем

class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=base_engine)

# --- МОДЕЛИ ---------------------------------------------------------


class City(Base):
    __tablename__ = "cities"

    #здесь записываем имеющиеся параметры
    id = Column(Integer, primary_key=True)
    full_name = Column(String, unique=True)

    universities = relationship("University", back_populates="city")
    programs = relationship("Program", back_populates="city")


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String) # Сокращение для упрощенного поиска
    ## здесь мы id для универа берем с city, поэтому когда будем делать запрос
    ## и искать вузы по городам - мы получим только с id Москвы
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="universities")
    programs = relationship("Program", back_populates="university")


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    university_id = Column(Integer, ForeignKey("universities.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    min_score = Column(String)
    budget_places = Column(String)
    subjects = Column(String)

    university = relationship("University", back_populates="programs")
    city = relationship("City", back_populates="programs")

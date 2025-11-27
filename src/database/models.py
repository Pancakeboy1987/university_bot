from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


base_engine = create_engine('sqlite:///database.db', echo=True)

class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=base_engine)

# --- МОДЕЛИ ---------------------------------------------------------


class City(Base):
    __tablename__ = "cities"

    #здесь записываем имеющиеся параметры
    id = Column(Integer, primary_key=True)
    full_name = Column(String, unique=True)
    name = Column(String,unique=True)

    ##здесь у нас лежат зависимости

    ## у нас универы и направления связаны с городами и могут брать данные
    universities = relationship("University", back_populates="city")
    programs = relationship("Program", back_populates="city")


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
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

    university = relationship("University", back_populates="programs")
    city = relationship("City", back_populates="programs")

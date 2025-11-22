# Src/Database.py
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Dynamic ideal functions table
IdealFunction = type('IdealFunction', (Base,), {
    '__tablename__': 'ideal_functions',
    'id': Column(Integer, primary_key=True),
    'x': Column(Float),
    **{f'y{i}': Column(Float) for i in range(1, 51)}
})

class TrainData(Base):
    __tablename__ = 'train_data'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    delta_y = Column(Float)
    ideal_function_no = Column(String)

class DatabaseHandler:
    def __init__(self, db_path='Output/idealFunctions.db'):
        os.makedirs('Output', exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_train_data(self, df):
        session = self.Session()
        for _, row in df.iterrows():
            session.add(TrainData(**row.to_dict()))
        session.commit()
        session.close()

    def insert_ideal_data(self, df):
        session = self.Session()
        for _, row in df.iterrows():
            data = {'x': row['x']}
            data.update({f'y{i}': row.get(f'y{i}') for i in range(1, 51)})
            session.add(IdealFunction(**data))
        session.commit()
        session.close()

    def insert_test_result(self, result):
        session = self.Session()
        session.add(TestResult(**result))
        session.commit()
        session.close()
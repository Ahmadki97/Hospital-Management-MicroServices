from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0938460904am@postgres/Users"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db  # Yield the session to be used in the route
    finally:
        db.close()


def createTable():
    print(f"Hello from CreateTable() Method")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables_name = ['Appointments']
    for table in tables_name:
        if table in metadata.tables:
            print(f"Table Already exists")
        else:
            print(f"Table Does Not Exist")
            Base.metadata.create_all(bind=engine)
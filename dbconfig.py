from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db=create_engine("sqlite:///data/data.sqlite")
DBBase=declarative_base(name="DBBase")
Session = sessionmaker(bind=db)

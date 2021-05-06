# Import Flask and dependencies
from flask import Flask, jsonify
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Database setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

inspector = inspect(engine)
inspector.get_table_names()
columns = inspector.get_columns("station")
print("========")
print("station")
print("======")
for column in columns:
    print(column["name"], column["type"])
print("======")
print("measurement")
print("====")
columns = inspector.get_columns("measurement")
for column in columns: 
    print(column["name"], column["type"])
# reflect an existing database into a new model
#base = automap_base()

# reflect the tables
#base.prepare(engine, reflect=True)

# Save references to each table
#measurement = base.classes.measurement
#station = base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)


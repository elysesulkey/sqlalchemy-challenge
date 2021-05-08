# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import pandas as pd
import datetime as dt
import re

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()

# Reflect the Tables
Base.prepare(engine, reflect=True)

#view
Base.classes.keys()

# Save References to Each Table
measurement = Base.classes.measurement
station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# List available routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii vacation planner!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation") 
#Convert query results to a dictionary using `date` as the key and `tobs` as the value
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query measurement
    results = (session.query(measurement.date, measurement.tobs)
                      .order_by(measurement.date))
    
    # Create a dictionary
    precip_date = []
    for row in results:
        date_dict = {}
        date_dict["date"] = row.date
        date_dict["tobs"] = row.tobs
        precip_date.append(date_dict)

    return jsonify(precip_date)


@app.route("/api/v1.0/stations") 
#Return a JSON list of stations from the dataset
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query stations
    results = session.query(station.name).all()

    # Convert list of tuples into normal list
    station_details = list(np.ravel(results))

    return jsonify(station_details)


@app.route("/api/v1.0/tobs") 
# Query the dates and temperature observations of the most active station for the last year of data
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query Measurements for latest date and calculate start date
    latest_date = (session.query(measurement.date)
                          .order_by(measurement.date
                          .desc())
                          .first())
    
    latest_date_str = str(latest_date)
    latest_date_str = re.sub("'|,", "",latest_date_str)
    latest_date_obj = dt.datetime.strptime(latest_date_str, '(%Y-%m-%d)')
    start_date = dt.date(latest_date_obj.year, latest_date_obj.month, latest_date_obj.day) - dt.timedelta(days=366)
     
    # Query station names and their observation counts sorted descending and select most active station
    station_list = (session.query(measurement.station, func.count(measurement.station))
                             .group_by(measurement.station)
                             .order_by(func.count(measurement.station).desc())
                             .all())
    
    station_act = station_list[0][0]
    print(station_act)


    # Return a list of tobs for the year before the final date
    tobs_results = (session.query(measurement.station, measurement.date, measurement.tobs)
                      .filter(measurement.date >= start_date)
                      .filter(measurement.station == station_act)
                      .all())

    # Create JSON results
    tobs_list = []
    for tobs_result in tobs_results:
        line = {}
        line["Date"] = tobs_result[1]
        line["Station"] = tobs_result[0]
        line["Temperature"] = int(tobs_result[2])
        tobs_list.append(line)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>") 
# Calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
def start_only(start):

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Date Range for 404 error
    date_max = session.query(measurement.date).order_by(measurement.date.desc()).first()
    date_max_str = str(date_max)
    date_max_str = re.sub("'|,", "",date_max_str)
    print (date_max_str)

    date_min = session.query(measurement.date).first()
    date_min_str = str(date_min)
    date_min_str = re.sub("'|,", "",date_min_str)
    print (date_min_str)


    # Check for valid entry of start date
    valid_entry = session.query(exists().where(measurement.date == start)).scalar()
 
    if valid_entry:

    	results = (session.query(func.min(measurement.tobs)
    				 ,func.avg(measurement.tobs)
    				 ,func.max(measurement.tobs))
    				 	  .filter(measurement.date >= start).all())

    	tmin =results[0][0]
    	tavg ='{0:.4}'.format(results[0][1])
    	tmax =results[0][2]
    
    	printout =( ['Start Date: ' + start,
    						'Lowest Temperature: '  + str(tmin) + ' F',
    						'Average Temperature: ' + str(tavg) + ' F',
    						'Highest Temperature: ' + str(tmax) + ' F'])
    	return jsonify(printout)

    return jsonify({"error": f"Date {start} not valid. Date Range is {date_min_str} to {date_max_str}"}), 404
   

@app.route("/api/v1.0/<start>/<end>") 
# Calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date 
def start_end(start, end):

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Date range for 404
    date_max = session.query(measurement.date).order_by(measurement.date.desc()).first()
    date_max_str = str(date_max)
    date_max_str = re.sub("'|,", "",date_max_str)
    print (date_max_str)

    date_min = session.query(measurement.date).first()
    date_min_str = str(date_min)
    date_min_str = re.sub("'|,", "",date_min_str)
    print (date_min_str)

    # Check for valid entry of start date
    valid_start = session.query(exists().where(measurement.date == start)).scalar()
 	
 	# Check for valid entry of end date
    valid_end = session.query(exists().where(measurement.date == end)).scalar()

    if valid_start and valid_end:

    	results = (session.query(func.min(measurement.tobs)
    				 ,func.avg(measurement.tobs)
    				 ,func.max(measurement.tobs))
    					  .filter(measurement.date >= start)
    				  	  .filter(measurement.date <= end).all())

    	tmin =results[0][0]
    	tavg ='{0:.4}'.format(results[0][1])
    	tmax =results[0][2]
    
    	printout =( ['Start Date: ' + start,
    						'End Date: ' + end,
    						'Lowest Temperature: '  + str(tmin) + ' F',
    						'Average Temperature: ' + str(tavg) + ' F',
    						'Highest Temperature: ' + str(tmax) + ' F'])
    	return jsonify(printout)

    if not valid_start and not valid_end:
    	return jsonify({"error": f"Start {start} and End Date {end} not valid. Date Range is {date_min_str} to {date_max_str}"}), 404

    if not valid_start:
    	return jsonify({"error": f"Start Date {start} not valid. Date Range is {date_min_str} to {date_max_str}"}), 404

    if not valid_end:
    	return jsonify({"error": f"End Date {end} not valid. Date Range is {date_min_str} to {date_max_str}"}), 404


if __name__ == '__main__':
    app.run(debug=True)
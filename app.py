import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


# database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# flask setup
app = Flask(__name__)


#create routes

#home page route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    """Return a list of precipitation data with dates"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

#station route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    """Return a list of dates and tobs for most active station"""
    # Query all tobs
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= last_year).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

#start and end date routes
#Define function for querying based on start date. Return TMAX, TMIN, and TAVG
def start_temp(start_date):

    session = Session(engine)

    return session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()

#Set app route and create dictionary and jsonify response
@app.route("/api/v1.0/<start>")
def start_date(start):
    starting_temp = start_temp(start)
    temps = list(np.ravel(starting_temp))
    
    temp_min = temps[0]
    temp_avg = temps[1]
    temp_max = temps[2]
    temp_dict = {'Min Temp': temp_min, 'Max Temp': temp_max, 'Avg Temp': temp_avg, 'Start Date': start}

    return jsonify(temp_dict)


#Define function for querying based on start and end date. Return TMIN, TMAX, and TAVG
def temps(start_date, end_date):
    session = Session(engine)

    return session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

#Set app route and create dictionary and jsonify response
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end_temp = temps(start, end)
    all_temp = list(np.ravel(start_end_temp))

    min_temp = all_temp[0]
    max_temp = all_temp[1]
    avg_temp = all_temp[2]
    
    all_temp_dict = {'Min Temp': min_temp, 
                    'Max Temp': max_temp, 
                    'Avg Temp': avg_temp, 
                    'Start Date': start, 
                    'End Date': end}

    return jsonify(all_temp_dict)

if __name__ == "__main__":
    app.run(debug=True)

























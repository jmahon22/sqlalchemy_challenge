import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Flask Setup
app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


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


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/temp/start/end")
def date(start = None, end = None):

    #variables
    start_date = start
    end_date = end

    session = Session(engine)

    #query for date & precipitation
    if end_date == None:
        maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
        minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    else:
        maxTemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date.filter(Measurement.date <= end_date)).scalar()
        minTemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date.filter(Measurement.date <= end_date)).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date.filter(Measurement.date <= end_date)).scalar()

    #dictionary
    weather_date = []
    weather_dict = {}
    weather_dict["Start Date"] = start_date
    weather_dict["End Date"] = end_date
    weather_dict["Max Temp"] = maxTemp
    weather_dict["Min Date"] = minTemp
    weather_dict["Avg Temp"] = avgTemp
    weather_date.append(weather_dict)

    return jsonify(weather_date)

    session.close()


if __name__ == "__main__":
    app.run(debug=True)

























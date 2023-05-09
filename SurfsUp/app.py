###############################################
###############################################
# Week 10 Challenge Part 2 API SQLite Connection & Landing Page

# Import Dependencies

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################


#1. / Start at the homepage.List all the available routes.
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start"
        f"api/v1.0/<start>/<end>"
    )

#2. /api/v1.0/precipitation- Convert the query results to a dictionary by using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def jsonified_prcp():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return prcpdata results"""
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=query_date).all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        date_dict= {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_prcp.append(date_dict)

    return jsonify(all_prcp)


#3. /api/v1.0/stations - Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def jsonified_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    results = session.query(Measurement.station).order_by(Measurement.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


#4. /api/v1.0/tobs - Query the dates and temperature observations of the most-active station for the previous year of data. ('USC00519281')
@app.route("/api/v1.0/tobs")
def jsonified_tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Query the dates and temperature observations for station USC00519281 in the past 12 Months"""
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results__temp_12m = session.query(Measurement.tobs , Measurement.date, Measurement.station).filter((Measurement.date>=query_date, Measurement.station =='USC00519281')).all()

    session = Session(engine)

    # Create a table of measurements
    tobs_rows = [{"Date": result[1], "tobs": result[0], "station": result[2]} for result in results__temp_12m]
    
    return jsonify(tobs_rows)


# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive

#5./api/v1.0/<start // /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start")
def Temperatures():
    """start"""
    return ()

if __name__ == "__main__":
    app.run(debug=True)

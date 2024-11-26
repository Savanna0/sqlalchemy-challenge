# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)
print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)

    start_date = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    last_date = dt.date(start_date.year, start_date.month, start_date.day)

    query_1 = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= last_date)\
    .order_by(Measurement.date).all()

    session.close()

    prcp_dict = dict(query_1)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)

    total_station_number = session.query(Station.station).all()

    session.close()

    station_names = list(np.ravel(total_station_number))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")

def temps():
    session = Session(engine)

    active_station_query = session.query(Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= '2016-08-23').all()

    session.close()

    temps_results = []
    for date, temps in active_station_query:
         temps_dict = {}
         temps_dict["Date"] = date
         temps_dict["Temps"] = temps
         temps_results.append(temps_dict)
    
    return jsonify(temps_results)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def start_end(start,end):
    session = Session(engine)

    start_end = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    starts_ends = []
    for min_temp, avg_temp, max_temp in start_end:
        start_end_dict = {}
        start_end_dict['Minimum Temperature'] = min_temp
        start_end_dict['Average Temperature'] = avg_temp
        start_end_dict['Maximum Temperature'] = max_temp
        temps.append(start_end_dict)

    return jsonify(starts_ends)
    

if __name__ == '__main__':
    app.run(debug=True)
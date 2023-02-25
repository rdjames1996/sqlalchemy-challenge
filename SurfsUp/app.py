import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
# create engine to hawaii.sqlite.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model.
Base = automap_base()

# reflect the tables.
Base.prepare(engine, reflect=True)

# Save references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB.
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Routes
@app.route("/")
def welcome():
    return (
        f"Welcome. Please view the available API routes below.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
# Query to get only last 12 months of data.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > "2016-08-23").\
        all()

    session.close()
    
    # Convert list of tuples into normal list
    monthly_data = list(np.ravel(results))
    return jsonify(monthly_data)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the Dataset.
   s_results = session.query(Measurement.station).all()
   s_list = list(np.ravel(s_results))
   return jsonify(s_list)
   
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    active = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-23").all()
    active_list = list(np.ravel(active))
    return jsonify(active_list)

##@app.route("/api/v1.0/<start>")
##def start(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.


if __name__ == "__main__":
    app.run(debug=True)
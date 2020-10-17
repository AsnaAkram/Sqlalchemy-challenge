import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
session = Session(engine)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start_dt>/<end_dt>"
    )


session.close


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year = query_date - dt.timedelta(days=365)

    past_temp = session.query(measurement.date, measurement.prcp).filter(
        measurement.date <= last_year).all()

    rainfall = {date: prcp for date, prcp in past_temp}
    return jsonify(rainfall)

    session.close()

    # Start of vacation page


@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine)
    start_only = (session.query(func.min(measurement.tobs),func.max
                                (measurement.tobs),func.avg(measurement.tobs))).\
                                    filter(measurement.date >= start).all()

    return jsonify(start_only)
    session.close()


@app.route("/api/v1.0/<start_dt><end_dt>")
def start(start_dt, end_dt):
    session = Session(engine)
    tobs_only = (session.query(func.min(measurement.tobs), func.max
                               (measurement.tobs), func.avg
                               (measurement.tobs))).filter(
        measurement.date >= start_dt).filter(measurement.date <= end_dt).all()

    return jsonify(tobs_only)
    session.close()

  # start page


@app.route("/api/v1.0/station")
def station1():
    session = Session(engine)
    station_nm = session.query(station.name, station.station).all()
    output = list(np.ravel(station_nm))
    return jsonify(output)
    session.close()


if __name__ == '__main__':
    app.run(debug=True)

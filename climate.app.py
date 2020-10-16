mport sqlalchemy
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
    return ("""<html><a href = "/api/v1.0/precipitation">/api/v1.0/precipitation</a>,
            <a href = "/api/v1.0/<start>">/api/v1.0/<start></a>,
            <a href = "/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end></a>
            <a href = /api/v1.0/station">/api/v1.0/station</a></html>"""

    )
session.close

@app.route("/api/v1.0/precipitation)
def precipitation():

    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year= query_date - dt.timedelta(days=365)

    past_temp=session.query(measurment.date,measuremnet.prcp).filter(measurment.date<=max_date).filter(measurment)
    !!!!!!

    rainfall={date:prcp for date, prcp in past_temp}
    return jasonify(rainfall)

    session.close()

    #Start of vacation page
@app.route("/api/v1.0/<start>")
def start(start=None):
    session = Session(engine)
    tobs_only= (session.query(measurment.tobs).filter(measurment.date.between(start,end)).all())

     return jsonify(tobs_only)
     session.close()

  #start page
@app.route("/api/v1.0/station")
def station():
   station=session.query(station.name, ststion.station).all()
   stations=list(np.ravel(ststions))
   return jsonify(stations)
   session.close()

if __name__ == '__main__':
    app.run(debug=True)
import os , sys
import pip
import json
from matplotlib.style import context
from flask import Flask , request
from flask import send_file , abort , render_template
from housing.exception import HousingException
from housing.logger import logging , get_log_dataframe
from housing.util.util import read_yaml_file , write_yaml_file
from housing.config.configuration import Configuration
from housing.pipeline.pipeline import Pipeline
from housing.entity.housing_predictor import HousingData , HousingPredictor



app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    
    try : 
        raise Exception ("We are trying custom exceptions")
    except Exception as e:
       housing =  HousingException(e , sys)
   
    logging.info(housing.error_message)
    logging.info("We are testing the logging module")
    return "This is the First Machine Learning Project"

if __name__ == "__main__":
    app.run(debug=True)

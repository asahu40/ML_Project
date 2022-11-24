from flask import Flask
from housing.exception import HousingException
from housing.logger import logging
import sys

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

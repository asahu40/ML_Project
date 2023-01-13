import os
import sys
import pandas as pd
from housing.exception import HousingException
from housing.util.util import load_object

class HousingData:

    def __init__(self , 
                 longitude : float,
                 latitude : float,
                 housing_median_age : float,
                 total_rooms : float,
                 total_bedrooms : float,
                 population : float,
                 households : float,
                 median_income : float,
                 ocean_proximity : str,
                 median_house_value : float = None
                 ):
    
        try :

            self.longitude = longitude
            self.latitude = latitude
            self.housing_median_age = housing_median_age
            self.total_rooms = total_rooms
            self.total_bedrooms = total_bedrooms
            self.population = population
            self.households = households
            self.median_income = median_income
            self.ocean_proximity = ocean_proximity
            self.median_house_value = median_house_value

        except Exception as e :
            raise HousingException(e,sys) from e 

    
    def get_housing_input_data_frame(self):

        try :
            housing_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
            
        except Exception as e :
            raise HousingException(e,sys) from e











from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
import os , sys



class DataValidation :

    def __init__ (self , data_validation_config : DataValidationConfig , data_ingestion_artifact : DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e :
            raise HousingException (e , sys) from e 

    def is_train_test_file_exists(self):
        try :
            logging.info("Checking if training and test file is available")
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_test_file_exists = os.path.exists(test_file_path)

            is_available = is_train_file_exists and is_test_file_exists
            logging.info(f"Is train and test file exists? -> {is_available}")

            if not is_available :
                train_file = self.data_ingestion_artifact.train_file_path
                test_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file : {train_file} or testing file : {test_file} is not present in the directory"
                logging.info(message)
                raise Exception (message)
                
            return is_available

        except Exception as e :
            raise HousingException (e,sys) from e 


    def validate_dataset_schema(self):
        try :
            pass
        except Exception as e :
            raise HousingException (e,sys) from e 


    def initiate_data_validation(self):
        try :
            is_available = self.is_train_test_file_exists()

            

        except Exception as e :
            raise HousingException (e,sys) from e 



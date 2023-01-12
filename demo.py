from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_transformation import DataTransformation
import os


def main():
    try :
        config_file_path = os.path.join("config" ,"config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_file_path))
        #pipeline.run_pipeline()
        pipeline.start()
        logging.info("Main Function Execution Completed")
        #data_ingestion_config = Configuration().get_data_ingestion_config()
        #print(data_ingestion_config)
        #data_validation_config = Configuration().get_data_validation_config()
        #print(data_validation_config)
        #data_transformation_config = Configuration().get_data_transformation_config()
        #print(data_transformation_config)
        
    except Exception as e :
        logging.error(f"{e}")
        print(e)


if __name__ == "__main__":
    main()





    
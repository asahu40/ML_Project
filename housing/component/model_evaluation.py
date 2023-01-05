from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.constant import *
import numpy as np
import os
import sys
from housing.util.util import read_yaml_file,write_yaml_file,load_data,load_object
from housing.entity.model_factory import evaluate_regression_model


class ModelEvaluation :

    def __init__ (self , model_evaluation_config = ModelEvaluationConfig,
                  data_ingestion_artifact = DataIngestionArtifact , 
                  data_validation_artifact = DataValidationArtifact , 
                  model_trainer_artifact = ModelTrainerArtifact):

        try :
            logging.info(f"{">"*20} Model Evaluation Log Started.{"<"* 20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e :
            raise HousingException (e,sys) from e

    def get_best_model(self):
        try :
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path)
                return model

            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY  not in model_eval_file_content:
                return model

            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY] )
            return model

        except Exception as e :
            raise HousingException (e,sys) from e 

    
    def update_evaluation_report (self , model_evaluation_artifact = ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content

            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content :
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous Eval Result :{model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY : {
                    MODEL_PATH_KEY : model_evaluation_artifact.evaluated_model_path
                }
            }

            if previous_best_model is not None :
                model_history = {self.model_evaluation_config.time_stamp : previous_best_model}
                if HISTORY_KEY not in model_eval_content :
                    history = {HISTORY_KEY : model_history}
                    eval_result.update(history)
                else :
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated Eval Result : {model_eval_content}")
            write_yaml_file(file_path=eval_file_path , data = model_eval_content)

        except Exception as e :
            raise HousingException (e,sys) from e 

    
    def initiate_model_evaluation(self)-> ModelEvaluationArtifact :
        try :
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path

            train_dataframe = load_data(file_path=train_file_path , schema_file_path=schema_file_path)
            test_dataframe = load_data(file_path=test_file_path , schema_file_path=schema_file_path)

            schema_content = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema_content[TARGET_COLUMN_KEY]

            ## Target Column :
            logging.info(f"Converting Target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion Completed target column into numpy array")

            ## Dropping Target column from the dataframe
            logging.info(f"Dropping Target column from the data frame")
            train_dataframe.drop(target_column_name , axis=1 , inplace=True)
            test_dataframe.drop(target_column_name , axis=1 , inplace=True)
            logging.info(f"Dropping Target Column from the data frame is completed")

            model = self.get_best_model()

            if model is None :
                logging.info(f"Not Found any existing model , Hence Accepting the trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path , is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model Accepted.Model Eval artifact{model_evaluation_artifact} created")
                return model_evaluation_artifact

                model_list = [model , trained_model_object]

                metric_info_artifact = evaluate_regression_model(model_list=model_list)


        
        except Exception as e :
            raise HousingException (e,sys) from e
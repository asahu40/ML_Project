from housing.config.configuration import Configuration
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelEvaluationConfig,ModelPusherConfig
from housing.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evaluation import ModelEvaluation
from housing.component.model_pusher import ModelPusher
from housing.constant import EXPERIMENT_DIR_NAME , EXPERIMENT_FILE_NAME
import os,sys

from collections import namedtuple
from datetime import datetime
from threading import Thread
from typing import List
import pandas as pd

Experiment = namedtuple("Experiment" , ["experiment_id" , "initialization_timestamp","artifact_time_stamp",
                                        "running_status" , "start_time" , "stop_time" ,"execution_time" , "message",
                                        "experiment_file_path" , "accuracy" , "is_model_accepted"])



class Pipeline(Thread) :

    experiment : Experiment  = Experiment(*([None]) *11) 
    experiment_file_path = None


    def __init__(self , config : Configuration = Configuration()) -> None :
        try :
            os.makedirs(config.training_pipline_config.artifact_dir , exist_ok=True)
            Pipeline.experiment_file_path = os.path.join(config.training_pipline_config.artifact_dir , EXPERIMENT_DIR_NAME , EXPERIMENT_FILE_NAME) 
            super().__init__(daemon=False , name="Pipeline")
            self.config = config
            
        except Exception as e :
            raise HousingException (e,sys) from e 


    def start_data_ingestion(self) -> DataIngestionArtifact :
        try :
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()

        except Exception as e :
            raise HousingException (e,sys) from e 

    def start_data_validation(self,data_ingestion_artifact : DataIngestionArtifact) -> DataValidationArtifact:
        try :
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config() ,
                                             data_ingestion_artifact=data_ingestion_artifact 
                                            )

            return data_validation.initiate_data_validation()

        except Exception as e :
            raise HousingException (e,sys) from e

    def start_data_transformation(self , data_ingestion_artifact : DataIngestionArtifact,
                                  data_validation_artifact : DataValidationArtifact
                                  ) -> DataTransformationArtifact:
        try :
            data_transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                     data_ingestion_artifact=data_ingestion_artifact,
                                                     data_validation_artifact=data_validation_artifact
                                                    )
            
            return data_transformation.initiate_data_transformation()

        except Exception as e :
            raise HousingException (e,sys) from e
        
    def start_model_trainer(self,data_transformation_artifact : DataTransformationArtifact) -> ModelTrainerArtifact:
        try :
            model_trainer = ModelTrainer(model_trainer_config = self.config.get_model_trainer_config(),
                                         data_transformation_artifact = data_transformation_artifact
                                        )

            return model_trainer.initiate_model_trainer()
            
        except Exception as e :
            raise HousingException (e,sys) from e

    def start_model_evaluation(self ,data_ingestion_artifact = DataIngestionArtifact,
                               data_validation_artifact = DataValidationArtifact ,
                               model_trainer_artifact = ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try :
            model_eval= ModelEvaluation(model_evaluation_config=self.config.get_model_evaluation_config(),
                                        data_ingestion_artifact=DataIngestionArtifact , 
                                        data_validation_artifact=DataValidationArtifact,
                                        model_trainer_artifact=ModelTrainerArtifact)
            
            return model_eval.initiate_model_evaluation()

        except Exception as e :
            raise HousingException (e,sys) from e 

    def start_model_pusher(self , model_eval_artifact = ModelEvaluationArtifact) -> ModelPusherArtifact:
        
        try :
            model_pusher = ModelPusher(self , model_pusher_config = self.config.get_model_pusher_config(), 
                                      model_evaluation_artifact=model_eval_artifact)

            return model_pusher.initiate_model_pusher()

        except Exception as e :
            raise HousingException (e,sys) from e 

    def run_pipeline(self):
        try :
            ## Data Ingestion 
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_tranformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                         data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_tranformation_artifact)
                                                             
            self.run_pipeline()

        except Exception as e :
            raise HousingException (e ,sys)from e 
 
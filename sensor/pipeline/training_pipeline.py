import os, sys
from sensor.components.data_ingestion import DataIngestion

from sensor.exception import SensorException
from sensor.logger import logging

# from sensor.components.data_ingestion import Da
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidationArtifact
from sensor.components.data_validation import DataValidation
from sensor.entity.config_entity import DataValidationConfig
from sensor.components.data_transformation import DataTransformation
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataTransformationArtifact


class TrainPipline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()
        

    def start_data_ingestion(self)->DataIngestionArtifact: #this function should return train and test file path as mentioned in artifact
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )

            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(
                data_ingestion_config = self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
            logging.info("Got the train_set and test_set from mongodb")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
                )
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e

    
    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    )-> DataTransformationArtifact:

        try:
            data_transformation = DataTransformation(
                data_validation_artifact, self.data_transformation_config
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

        
    

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact
            )

            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact
            )
        except Exception as e:
            raise SensorException(e, sys)

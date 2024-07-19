# MercaditoNicaAIModels

## Overview

MercaditoNicaAIModels is a project developed as part of the MercaditoNica platform. It focuses on building and deploying artificial intelligence models to enhance the platform's functionality, including product recommendations, market analysis and pricing suggestions. The project is organized into various components including data handling, model development, training, evaluation, and Docker containerization.

## Project Structure

- **/data/**: Contains scripts for loading, cleaning, and splitting data.
  - `data_loader.py`: Scripts for loading and preprocessing data.
  - `data_cleaning.py`: Data cleaning and transformation scripts.
  - `data_splitting.py`: Scripts for splitting data into training/testing sets.

- **/models/**: Contains the AI model scripts and utility functions.
  - `model_1.py`: First AI model script.
  - `model_2.py`: Second AI model script.
  - `model_3.py`: Third AI model script.
  - `model_utils.py`: Utility functions for model training and evaluation.

- **/scripts/**: Contains scripts for training, evaluating, and predicting with models.
  - `train_models.py`: Script to train all models.
  - `evaluate_models.py`: Script to evaluate model performance.
  - `predict.py`: Script for making predictions with trained models.

- **/notebooks/**: Jupyter notebooks for data analysis and model training.
  - `exploratory_analysis.ipynb`: Jupyter notebook for exploratory data analysis.
  - `model_training.ipynb`: Jupyter notebook for model training and tuning.

- **/tests/**: Contains tests for the project.
  - `test_data_loader.py`: Tests for data loading and preprocessing.
  - `test_models.py`: Tests for model functionality.
  - `test_utils.py`: Tests for utility functions.

- **/configs/**: Configuration files for the project.
  - `config.yaml`: Configuration file for model parameters and settings.
  - `logging.yaml`: Configuration file for logging.

- **/docs/**: Documentation files for the project.
  - `design_document.md`: Documentation of the model design and architecture.
  - `user_guide.md`: Documentation for using the models.

- **/logs/**: Logs related to model training.
  - `training.log`: Logs related to model training.

- **/docker/**: Docker-related files for containerizing the project.
  - `Dockerfile`: Dockerfile for building the AI models image.
  - `docker-compose.yml`: Docker Compose file for managing multi-container Docker applications.
  - `entrypoint.sh`: Script to set up the environment and start the application.

- **requirements.txt**: Python dependencies for the project.
- **setup.py**: Setup script for installing the package.
- **README.md**: This file.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

install requirements
pip install -r requirements.txt


Usage
Training Models:

To train all models, run:
python scripts/train_models.py


Evaluating Models:

To evaluate model performance, run:
python scripts/evaluate_models.py

Making Predictions:

To make predictions with a trained model, run:
python scripts/predict.py

To make predictions with a trained model, run:
python scripts/evaluate_models.py

Build the docker image:
docker build -t mercaditonica-ai-models -f docker/Dockerfile .

Run the Docker container:
docker-compose up

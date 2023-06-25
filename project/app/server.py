from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
import logging

from classifier import NewsCategoryClassifier


class PredictRequest(BaseModel):
    source: str
    url: str
    title: str
    description: str


class PredictResponse(BaseModel):
    scores: dict
    label: str


MODEL_PATH = "../data/news_classifier.joblib"
LOGS_OUTPUT_PATH = "../data/logs.out"

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    [TO BE IMPLEMENTED]
    1. Initialize an instance of `NewsCategoryClassifier`.
    2. Load the serialized trained model parameters (pointed to by `MODEL_PATH`) into the NewsCategoryClassifier you initialized.
    3. Open an output file to write logs, at the destimation specififed by `LOGS_OUTPUT_PATH`
        
    Access to the model instance and log file will be needed in /predict endpoint, make sure you
    store them as global variables
    """
    global log_file
    global classifier_model

    classifier_model = NewsCategoryClassifier()
    classifier_model.load(model_path=MODEL_PATH)
    

    # Create a file to write logs to a file
    log_file = open(LOGS_OUTPUT_PATH, 'a+')
    # logger.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s: %(message)s"))
    # logger.addHandler(log_file)
    logger.info("Logger initialized")

    logger.info("Setup completed")


@app.on_event("shutdown")
def shutdown_event():
    # clean up
    """
    [TO BE IMPLEMENTED]
    1. Make sure to flush the log file and close any file pointers to avoid corruption
    2. Any other cleanups
    """
    log_file.close()
    logger.info("Shutting down application")


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # get model prediction for the input request
    # construct the data to be logged
    # construct response
    """
    [TO BE IMPLEMENTED]
    1. run model inference and get model predictions for model inputs specified in `request`
    2. Log the following data to the log file (the data should be logged to the file that was opened in `startup_event`)
    {
        'timestamp': <YYYY:MM:DD HH:MM:SS> format, when the request was received,
        'request': dictionary representation of the input request,
        'prediction': dictionary representation of the response,
        'latency': time it took to serve the request, in millisec
    }
    3. Construct an instance of `PredictResponse` and return
    """
    import time
    import json
    import datetime

    time_initiated = datetime.datetime.now()
    start = time.time()
    pred = classifier_model.predict_label(request)
    probs = classifier_model.predict_proba(request)
    response = PredictResponse(scores=probs, label=pred)
    end = time.time()
    elapsed = (end-start) * 1000

    log_info = {
        'timestamp': time_initiated.strftime("%Y:%m:%d %H:%M:%S"),
        'request': request,
        'prediction': response,
        'latency': elapsed
    }   

    # log_file.write(f'{json.dumps(log_info)}\n')
    log_file.write(str(log_info))
    log_file.write('\n')
    log_file.flush()
    logger.info(log_info)

    # response = PredictResponse(scores={"label1": 0.9, "label2": 0.1}, label="label1")

    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}

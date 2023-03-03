from neurosity import neurosity_sdk
from dotenv import load_dotenv
import os

load_dotenv()

timestamp = 0

neurosity = neurosity_sdk({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD"),
})


def callbackRight(data):
    global timestamp
    prob = data['predictions'][0]['probability']
    ts = data['predictions'][0]['timestamp']
    if prob > 0.8 and ts - timestamp > 5000:
        print("moving right")
        timestamp = ts


def callbackLeft(data):
    global timestamp
    prob = data['predictions'][0]['probability']
    ts = data['predictions'][0]['timestamp']
    if prob > 0.8 and ts - timestamp > 5000:
        print("moving left")
        timestamp = ts


unsubscribeRight = neurosity.kinesis("rightArm", callbackRight)
unsubscribeLeft = neurosity.kinesis("leftArm", callbackLeft)

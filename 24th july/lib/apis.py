import requests
from pymongo import MongoClient
import json
# from env import *
import logging

# API Urls
CHECK_USER_URL = "https://mybafozmf8.execute-api.us-east-1.amazonaws.com/dev/checkUser"
REGISTRATION_URL = "https://mybafozmf8.execute-api.us-east-1.amazonaws.com/dev/registerUser"
DEREGISTER_USER = "https://mybafozmf8.execute-api.us-east-1.amazonaws.com/dev/deRegister"



def deregister_user(id):
	body = {
		"id": id
	}
	headers = {"Content-Type": "application/json"}
	response = requests.post(
		url= DEREGISTER_USER, data=json.dumps(body), headers=headers)
	try:
		data = response.json()
		logging.info("CANCEL API RESPONSE: "+str(data))
		return data
	except:
		return None


def verify_user(phone, platform):
    platform_json = {
        "whatsapp": "W",
        "ios": "I",
        "android": "A",
        "facebook": "F",
        "telegram": "T",
        "web": "B",
        "Browser": "B",
        "mobile": "A"

    }

    body = {
        "mobile_no": phone,
        "platform": platform_json[platform]
        # "platform": "W"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        url=CHECK_USER_URL, data=json.dumps(body), headers=headers)
    # url="https://k19up7hlj5.execute-api.ap-south-1.amazonaws.com/dev/checkUser", data=json.dumps(body), headers=headers)
    try:
        data = response.json()
        logging.info("VERIFY USER API RESPONSE: " + str(data))
        return data
    except:
        return None


def register(name, phone):
    body = {
        "mobile_no": phone,
        "first_name": name
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url=REGISTRATION_URL, data=json.dumps(body), headers=headers)
    try:
        data = response.json()
        logging.info("REGISTER API RESPONSE: " + str(data))
        return data
    except:
        return None




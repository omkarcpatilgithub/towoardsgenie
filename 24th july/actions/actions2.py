
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import pymongo
import re
from lib import apis


class ActionFindMongo(Action):

    def name(self) -> Text:
        return "actions_find_in_mongo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        facility = tracker.get_slot("facility_type")
        area = tracker.get_slot("location")

        print(tracker.sender_id)
        session = tracker.sender_id
        print(type(session))

        link = 'mongodb://localhost:27017'
        cluster = MongoClient(link)
        db = cluster["rasa"]
        collection = db["rasa"]



        ######### calling API to check in db #########

        session = tracker.sender_id
        print("session: "+session)
        phoneNumRegex = re.compile(r'[0-9]*')
        mo = phoneNumRegex.search(session)
        phone = mo.group()
        print(mo.group())

        platform = re.compile(r'[a-zA-Z]+')
        mo = platform.search(session)
        platform = mo.group().lower()

        response = apis.verify_user(phone, platform)
        print(response)
        ##################################


        #####  chekcking whether user exist in local mongo db #########
        results = collection.find({"session": session})
        ##################################################

        ### if user is not register then if will perform
        if (results.count() == 0):
            message = 'you are not registered'
            print(message)
            # dispatcher.utter_message(text=message)
            return [FollowupAction("action_form_ask_name")]

        ### if user is registered then else
        else:
            # print(results[0]['name'])

            # print(tracker.latest_message)
            user = results[0]['name']
            dispatcher.utter_message(text="Hello {}, tell me how can i help you".format(user))
            return []   #TODO add followupAction for extra confirmation



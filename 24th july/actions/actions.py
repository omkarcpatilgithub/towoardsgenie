# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import pymongo


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ############# add this to every code at start of every action funtion, so any unregistered user will go to registration 1st #############
        session = tracker.sender_id
        link = 'mongodb://localhost:27017'
        cluster = MongoClient(link)
        db = cluster["rasa"]
        collection = db["rasa"]
        results = collection.find({"session": session})
        if (results.count() == 0):
            message = 'you are not registered, please tell me your name'
            print(message)
            # dispatcher.utter_message(text=message)
            return [FollowupAction("action_form_ask_name")]
        ############# ############# ############# ############# ############# ############# ############# #############

        facility = tracker.get_slot("facility_type")
        area = tracker.get_slot("location")


        if(facility == 'hospital'):
            if(area == 'sitka'):
                add = 'fortis, sitka'
            if(area == 'juneau'):
                add = 'fortis, juneau'
        elif(facility == 'restaurant'):
            if(area == 'sitka'):
                add = '4 seasons, sitka'
            if(area == 'juneau'):
                add = '4 seasons, juneau'



        #add = "300 hyde st, sitka"
        dispatcher.utter_message(text="Here is address for {} in {}: {}".format(facility, area, add))

        return [SlotSet("address", add)]



    class ActionLocation(Action):

        def name(self) -> Text:
            return "action_ask_location"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            ############# add this to every code at start of every action funtion, so any unregistered user will go to registration 1st #############
            session = tracker.sender_id
            link = 'mongodb://localhost:27017'
            cluster = MongoClient(link)
            db = cluster["rasa"]
            collection = db["rasa"]
            results = collection.find({"session": session})
            if (results.count() == 0):
                message = 'you are not registered, please tell me your name'
                print(message)
                # dispatcher.utter_message(text=message)
                return [FollowupAction("action_form_ask_name")]
            ############# ############# ############# ############# ############# ############# ############# #############


            # add = "300 hyde st, sitka"
            dispatcher.utter_message(text="Could your please tell me your location")

            return []
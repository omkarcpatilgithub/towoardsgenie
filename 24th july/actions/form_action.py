
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import re
from lib import apis

class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_form_ask_name"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        # if (tracker.get_slot("confirmation") == "N" or tracker.get_slot("confirmation") is None):
        return ["name", "email", "confirmation","updation"]
        # else:
        #     return []



## how is this returning form intent
    ## got it, check nlu.md once

    def slot_mappings(self) -> Dict[Text, Any]:
        # return {"name": self.from_entity(entity="name",
        #                                  intent=["name"]),


        return {"name": [self.from_text(intent=["name"])],
                "email": [self.from_text(intent=["email"])],
                "confirmation": [self.from_intent(intent=["affirm"], value= "Y"),self.from_intent(intent=["deny"], value= "N")],
                "updation": [self.from_text(intent=["updation"])]}



    def validate_updation(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if( value in ("1",'1st','1st one','1st One','name')):
            return {"name": None, "updation": "name"}

        elif (value in ("2", '2nd', '2nd one', '2nd One', 'email')):
            return {"email": None, "updation": "email"}

        elif (value in ("3", '3rd', '3rd one', '3rd One', 'both')):
            return {"name": None, "email": None, "updation": "both"}

        else:
            return {}



    def validate_confirmation(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        print("confirmation value: "+value)


        if (value == "N"):
            print("inside if confirmation value N")
            return {"confirmation": value}
           # return {"name": None,"email": None,"confirmation": None}

        else:
            print("inside else confi else")
            return {"confirmation": value, "updation": "not needed"}



    def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""


        print('########################################3')
        print(tracker.slots)
        print('########################################3')
        # print(tracker.latest_message)


        print(tracker.latest_action_name)
        if (tracker.slots['name']):
            value = tracker.slots['name']
        print('returning whole value')
        return {"name": value}

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        print(tracker.slots)
        pattern = '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'

        if(re.match(pattern, value)):
            return {"email": value}
        else:
            dispatcher.utter_template("utter_ask_email", tracker)
            return {"email": None}



        # if len(value) > 2:
        #     sender_id = tracker.sender_id
        #     slotStorage.set_slot(sender_id, "name", value)
        #     return {"name": value}
        # else:
        #     dispatcher.utter_template("utter_ask_name", tracker)
        #     return {"name": None}
        

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')

        ## connecting to mongo db
        link = 'mongodb://localhost:27017'
        cluster = MongoClient(link)
        db = cluster["rasa"]
        collection = db["rasa"]

        print(tracker.sender_id, name, email)

        ## inserting to Mongo db
        post = {"session": tracker.sender_id, "name": name, "email": email}
        collection.insert_one(post)

        ## inserting to GM db with api call

        session = tracker.sender_id
        phoneNumRegex = re.compile(r'[0-9]*')
        mo = phoneNumRegex.search(session)
        phone = mo.group()
        print(mo.group())
        response = apis.register(name, phone)




        # dispatcher.utter_message(text="Please confirm following information \nname: {},  \nemail: {}\n".format(name,email))

        return [FollowupAction("actions_find_in_mongo")]
        # return [FollowupAction("action_confirm_form")]




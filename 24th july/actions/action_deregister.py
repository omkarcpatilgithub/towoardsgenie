# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import pymongo
# from pymongo import MongoClient
# from rasa_sdk.events import SlotSet, FollowupAction
# import pymongo
#
#
# class ActionDeregister(Action):
#
#     def name(self) -> Text:
#         return "actions_deregister"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#
#         print(tracker.sender_id)
#         session = tracker.sender_id
#
#         link = 'mongodb://localhost:27017'
#         cluster = MongoClient(link)
#         db = cluster["rasa"]
#         collection = db["rasa"]
#
#         results = collection.find({"session": session})
#         user = results[0]['name']
#         collection.delete_many({"session": session})
#
#         dispatcher.utter_message(text="ok {}, your number is deregistered from our system \n hope to see you again soon".format(user))
#
#         return [SlotSet("name", None), SlotSet("email", None)]


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import re
from lib import apis


class action_deregister(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "actions_deregister"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        # if (tracker.get_slot("confirmation") == "N" or tracker.get_slot("confirmation") is None):
        return ["deregister_confirmation"]
        # else:
        #     return []

    ## how is this returning form intent
    ## got it, check nlu.md once

    def slot_mappings(self) -> Dict[Text, Any]:
        # return {"deregister_confirmation": [self.from_text()]}

        # self.from_entity(entity=entity_name, intent=intent_name

        return {
            "deregister_confirmation": [self.from_text(intent=["affirm","number"]),
                                        self.from_text(intent=["deny","number"])]
        }


    def validate_deregister_confirmation(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        # print('########################################3')
        # print(tracker.latest_message["intent"])


        intent_name = tracker.latest_message["intent"]["name"]

        if (value == "1" or intent_name == "affirm"):
            return {"deregister_confirmation": "yes"}
        elif (value == "2" or intent_name == "deny"):
            return {"deregister_confirmation": "no"}
        else:
            return {"deregister_confirmation": None}


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""
        sender_id = tracker.sender_id
        deregister_confirmation = tracker.get_slot("deregister_confirmation")

        if (deregister_confirmation == "yes"):

            ######### calling API to check in db #########

            session = tracker.sender_id
            print("session: " + session)
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

            id = response['data'][0]['_id']
            print("########### ID ###########")
            print(id)


            # response = apis.deregister_user()

        dispatcher.utter_message(text="Hello user, your selections are session: {} and deregistration confirm {}".format(sender_id,deregister_confirmation))

        return [SlotSet("deregister_confirmation", None)]






from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import pymongo
import re
from lib import apis


class ActionMenu(Action):

    def name(self) -> Text:
        return "actions_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        name = tracker.get_slot("name")
        dispatcher.utter_message(text="Hello {},\n tell me How can I assist you? Please choose one of the following options: \n1. Find a business\n2. My Account\n3. Spread the magic ".format(name))

        return []
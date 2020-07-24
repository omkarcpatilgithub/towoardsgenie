## showing menu
* greet
  - actions_find_in_mongo
* menu
  - actions_menu

## deregistering accont
* deregister
  - actions_deregister

## mongo exist
* find_in_mongo
  - actions_find_in_mongo
* thanks
 - utter_goodbye
 
 
## search hospital happy path
* greet
  - actions_find_in_mongo
* search_provider{"facility_type": "hospital", "location": "San francisco"}
  - action_facility_search
  - slot{"address": "300 hyde"}
* thanks
  - utter_goodbye
 
## search hospital + location
* greet
  - actions_find_in_mongo
* search_provider{"facility_type":"hospital"}
  - action_ask_location
* inform{"location": "San francisco"}
  - action_facility_search
  - slot{"address": "300 hyde road"}
* thanks
  - utter_welcome
  - utter_goodbye
  
## happy path
* greet
  - actions_find_in_mongo
* mood_great
  - utter_happy

## sad path 1
* greet
  - actions_find_in_mongo

* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - actions_find_in_mongo
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help


## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

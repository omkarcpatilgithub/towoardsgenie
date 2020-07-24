
## to start rasa nlu and core (on port 5066)
rasa run --endpoints endpoints.yml --credentials credentials.yml --enable-api -p 5066 --debug

## to run actions server (on port 5055)
rasa run actions --actions actions -p 5055 --debug

## to start nlg server (not needed in this case)
python nlg_server.py --domain domain.yml

5f16efcc90d8c5e1333f6e55


curl -X POST -F "session=918425017010-WhatsApp" -F "message=deregister" http://localhost:5066/webhooks/NihkaBot/webhook



curl -X POST -F "session=918425017010-WhatsApp" -F "message=hello" http://localhost:5066/webhooks/NihkaBot/webhook
curl -X POST -F "session=918425017010-WhatsApp" -F "message=you can call me amma" http://localhost:5066/webhooks/NihkaBot/webhook
curl -X POST -F "session=918425017010-WhatsApp" -F "message=ocpatil@gmail.com" http://localhost:5066/webhooks/NihkaBot/webhook
curl -X POST -F "session=918425017010-WhatsApp" -F "message=correct" http://localhost:5066/webhooks/NihkaBot/webhook


curl -X POST -F "session=davidnew" -F "message=i need hospital in sitka" http://localhost:5066/webhooks/NihkaBot/webhook


curl -X POST -F "session=david" -F "message=hello" http://localhost:5066/webhooks/NihkaBot/webhook

curl -X POST -F "session=david" -F "message=i need a hospital" http://localhost:5066/webhooks/NihkaBot/webhook
juneau
curl -X POST -F "session=davidnew" -F "message=juneau" http://localhost:5066/webhooks/NihkaBot/webhook

curl -X POST -F "session=david" -F "message=thank you" http://localhost:5066/webhooks/NihkaBot/webhook
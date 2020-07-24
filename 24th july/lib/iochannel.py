# from rasa.core.channels.channel import RestInput
# from rasa.core.channels.channel import UserMessage
#
# class ScratchBot(RestInput):
#
#     @classmethod
#     def name(cls):
#         print('hi in name method')
#         return "ScratchBot"
#
#     async def _extract_sender(self, req):
#         return req.form.get("session", None)
#
#     # noinspection PyMethodMayBeStatic
#     def _extract_platform(self, req):
#         return req.form.get("platform", None)
#
#     # noinspection PyMethodMayBeStatic
#     def _extract_message(self, req):
#         return req.form.get("message", None)
#
#
#
#
#
#     def blueprint(self, on_new_message):
#         custom_webhook = Blueprint(
#             "custom_webhook_{}".format(type(self).__name__),
#             inspect.getmodule(self).__name__,
#         )
#
#         # noinspection PyUnusedLocal
#         @custom_webhook.route("/", methods=["GET"])
#         async def health(request: Request):
#             return response.json({"status": "ok"})
#
#     @custom_webhook.route("/webhook", methods=["POST"])
#     async def receive(request: Request):
#         sender_id = await self._extract_sender(request)
#         input_channel = self._extract_platform(request)
#         text = self._extract_message(request)


from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import boto3
from datetime import datetime
from random import randint
import inspect
import requests
# import lib.constants as constants
# import requests_async as requests
import pymongo
import pymongo
from pymongo import MongoClient



from rasa.core.channels.channel import RestInput
from rasa.core import utils
from rasa.core import agent
from rasa.core.interpreter import RasaNLUInterpreter
from rasa.core.channels.channel import UserMessage
from rasa.core.channels.channel import CollectingOutputChannel
from rasa.core import utils
import rasa.utils.endpoints
from rasa_sdk.events import SlotSet
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from asyncio import Queue, CancelledError
# from flask import jsonify
import asyncio

logger = logging.getLogger(__name__)


class NihkaBot(RestInput):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "NihkaBot"   # this name you need to mention in endpoint.yml file


    #########  Extracting information from user         ########################
    #####  here session and message is must, though you can extract any other even user is not passing it
    async def _extract_sender(self, req):
        return req.form.get("session", None)

    # noinspection PyMethodMayBeStatic
    def _extract_platform(self, req):
        return req.form.get("platform", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req):
        return req.form.get("message", None)

    # noinspection PyMethodMayBeStatic
    def _extract_attachment(self, req):
        return req.form.get("attachment[0]", None)

    ##############################################


    ####################### message transfer from iochannel to rasa core ##############################################

    ## user sent message and other info will be wraped here and sent to core
    @staticmethod
    async def on_message_wrapper(on_new_message, text, queue, sender_id):
        collector = QueueOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, input_channel=RestInput.name()
        )
        await on_new_message(message)   ## TODO  find details about this functions      # func sends message to core

        await queue.put("DONE")

    ## waits for the response from the core
    def stream_response(self, on_new_message, text, sender_id):
        async def stream(resp):
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(on_new_message, text, q, sender_id)
            )
            while True: # wait until the message doesnt come
                result = await q.get()
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream

    ##########################################################################################################################################


    ####################### This is main function, here we will write our business logic for get and post methods #######################
    def blueprint(self, on_new_message):
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"]) # for get method on core's link

        async def health(request: Request):
            return response.json({"status": "ok"})

## for all post request
        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            ## extract required data
            print(request.form)
            sender_id = await self._extract_sender(request)
            input_channel = self._extract_platform(request)
            text = self._extract_message(request)


            attachment = self._extract_attachment(request)
            if attachment != None:
                text = attachment

            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )



## sends message in to rasa core
            if should_use_stream:
                return response.stream(
                    self.stream_response(on_new_message, text, sender_id),
                    content_type="text/event-stream",
                )
            else:

                collector = CollectingOutputChannel()
                print('1st collector.message')
                print(collector.messages)
                print(type(collector.messages))
                # noinspection PyBroadException
                try:
                    await on_new_message(
                        UserMessage(
                            text, collector, sender_id, input_channel=input_channel
                        )
                    )

                    print('2nd after await onnewmessage collector.message')
                    print(collector.messages)
                    print(type(collector.messages))

                    message_received_is = collector.messages[0]
                    text = message_received_is.get("text")
                    print(text)
                    recipient_id = message_received_is.get("recipient_id")


                    message = {
                        "success": 1,
                        "message": [
                            {
                                "message": {
                                    "template": {
                                        "elements": {
                                            "title": text,
                                            "says": "",
                                            "visemes": ""
                                        }
                                    }
                                }
                            }
                        ],
                        "session": sender_id
                    }

                    #
                    # message = {
                    #     "success": 1,
                    #     "message": text,
                    #     "session": recipient_id
                    # }
                    print('#############printing message reply to talkk#################')
                    print(message)
                    return response.json(message)



                except CancelledError:
                    logger.error(
                        "Message handling timed out for "
                        "user message '{}'.".format(text)
                    )
                except Exception:
                    logger.exception(
                        "An exception occured while handling "
                        "user message '{}'.".format(text)
                    )
            # return response.json(message)

        return custom_webhook



    # def blueprint(self, on_new_message):
    #     custom_webhook = Blueprint(
    #         "custom_webhook_{}".format(type(self).__name__),
    #         inspect.getmodule(self).__name__,
    #     )
    #
    #     # noinspection PyUnusedLocal
    #     @custom_webhook.route("/", methods=["GET"])
    #     async def health(request: Request):
    #         return response.json({"status": "ok"})
    #
    #     @custom_webhook.route("/webhook", methods=["POST"])
    #     async def receive(request: Request):
    #         sender_id = await self._extract_sender(request)
    #         input_channel = self._extract_platform(request)
    #         text = self._extract_message(request)
    #
    #         # get the selection index value if selection index is selected.
    #         text = await self.get_selection_index_value(sender_id, text)
    #
    #         attachment = self._extract_attachment(request)
    #         if attachment != None:
    #             text = attachment
    #
    #         should_use_stream = rasa.utils.endpoints.bool_arg(
    #             request, "stream", default=False
    #         )
    #
    #         if should_use_stream:
    #             return response.stream(
    #                 self.stream_response(on_new_message, text, sender_id),
    #                 content_type="text/event-stream",
    #             )
    #         else:
    #             collector = CollectingOutputChannel()
    #             # noinspection PyBroadException
    #             try:
    #                 await on_new_message(
    #                     UserMessage(
    #                         text, collector, sender_id, input_channel=input_channel
    #                     )
    #                 )
    #
    #                 message_received_is = collector.messages[0]
    #                 text = message_received_is.get("text")
    #                 text = json.loads(text)  # convert the string to json
    #                 recipient_id = message_received_is.get("recipient_id")
    #
    #                 # Set the selection index in the tracker, based on the request_slot.
    #                 await self.set_selection_index(recipient_id)
    #
    #                 # Get the platform of the user and accordingly decide on generating ssmls
    #                 platform = await self.get_platform(recipient_id)
    #
    #                 # check if message alreday has as ssml says
    #                 for i in text:
    #                     if "ssml" in i:
    #                         if text[0]['message']['template']['elements']['says'] != "" and \
    #                                 text[0]['message']['template']['elements']['visemes'] != "":
    #                             ssml = "ssml already added"
    #                             break
    #                         else:
    #                             ssml = i["ssml"]
    #                             break
    #                     else:
    #                         ssml = "No ssml"
    #
    #                 if platform == "Whatsapp" or ssml == "No ssml" or ssml == "ssml already added":
    #                     message = {
    #                         "success": 1,
    #                         "message": text,
    #                         "session": recipient_id
    #                     }
    #                     return response.json(message)
    #                 else:
    #                     message = self.get_voice_and_visemes(text, recipient_id)
    #
    #             except CancelledError:
    #                 logger.error(
    #                     "Message handling timed out for "
    #                     "user message '{}'.".format(text)
    #                 )
    #             except Exception:
    #                 logger.exception(
    #                     "An exception occured while handling "
    #                     "user message '{}'.".format(text)
    #                 )
    #             return response.json(message)
    #
    #     return custom_webhook


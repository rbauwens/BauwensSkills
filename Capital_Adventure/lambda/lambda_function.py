# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# just finished step 4 of https://developer.amazon.com/en-US/alexa/alexa-skills-kit/resources/training-resources/cake-walk
# make changes here then click save and deploy. then you can go to the test tab
# to add new keywords (like location) you need to add an intent in the Build tab
# then you would add a new intent handler to listen for that key world
# Todo: i'm not sure how the question and answers are linked

QUESTIONS = { 
    "France": [
        {
            "What is the capital of France?":
            ["Paris", "Rome", "London"]
        }
    ],
    "Germany": [
        {
            "In which city is the Brandenburg Gate?":
            ["Berlin", "Munich", "Hamburg"]
        }
    ]
}

GREETINGS = [
    {
        "France": "Bonjour",
        "Germany": "Guten Tag"
    }
]

class GameState():
    first_question = None
    location = ""
    correct_answer = ""
    correct_answer_text = ""
    
    def set_correct_answer(self, answer):
        self.correct_answer = answer

GAMESTATE = GameState()

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    # canHandle() function is where you define what requests the handler responds to.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

   #  The handle() function returns a response to the user.
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        GAMESTATE.first_question = True

        speak_output =  "Hello! Welcome to Capital Adventure! \
        Where in the world are you?"

        reprompt_text = "To get the next question tell me where you are on the board"
        
        return(handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request using resolutions."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return (request.intent.slots[slot_name].resolutions.
                resolutions_per_authority[0].values[0].value.name)
    except (AttributeError, ValueError, KeyError, IndexError):
        return None


class CaptureLocationIntentHandler(AbstractRequestHandler):
    """Handler for Location Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        if not ask_utils.is_intent_name("CaptureLocationIntent")(handler_input):
            return False

        is_location = False
        if (handler_input.request_envelope.request.intent.slots["Location"] is not None):
            is_location = True
        return is_location
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots
        location = slots["Location"].value
        greeting = GREETINGS[0][location]
        
        speak_output = "{}. Now I will ask you a question about {}. ".format(greeting, location)
        
        if (GAMESTATE.first_question):
            speak_output = speak_output + "When you're ready to answer, say, the answer is, and the letter of the answer. "
            GAMESTATE.first_question = False
        
        question = QUESTIONS[location][0]

        for x in list(question)[0:1]:
            next_question = x
            correct_answer = question[x][0]
            local_answers = question[x] 
            random.shuffle(local_answers)
            correct_answer_letter = local_answers.index(correct_answer)
            GAMESTATE.correct_answer_text = correct_answer
            
            if (correct_answer_letter == 0):
                GAMESTATE.correct_answer = "a"
            elif (correct_answer_letter == 1):                         
                GAMESTATE.correct_answer = "b"
            elif (correct_answer_letter == 2):  
                GAMESTATE.correct_answer = "c"

        answer_format_text = " Is it a: {}, b: {}, or c: {}".format(local_answers[0], local_answers[1], local_answers[2])

        question_text = next_question + answer_format_text
        
        speak_output = speak_output + question_text
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    """Handler for answer intent."""

    # canHandle() function is where you define what requests the handler responds to.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        if not ask_utils.is_intent_name("AnswerIntent")(handler_input):
            return False

        is_answer = False
        if (handler_input.request_envelope.request.intent.slots["Answer"] is not None):
            print("value is an answer")
            is_answer = True
        else:
            print("value is not an answer")
        return is_answer

   #  The handle() function returns a response to the user.
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        given_answer = handler_input.request_envelope.request.intent.slots["Answer"].value
        speak_output =  "I heard your answer"
        if(given_answer == GAMESTATE.correct_answer):
            speak_output =  "Well done! Your answer, {}, was correct!".format(given_answer)
        else:
            print("GAMESTATE.correct_answer: {}".format(GAMESTATE.correct_answer))
            speak_output =  "Bad luck, your answer, {}, was incorrect. The correct answer was {}: {}".format(given_answer, GAMESTATE.correct_answer, GAMESTATE.correct_answer_text)

        return(handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureLocationIntentHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
from typing import Text, List, Any, Dict
import datetime as dt

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_PIZZA_SIZES = ["small", "medium", "large",
                       "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PIZZA_TYPES = ["mozzarella", "fungi", "veggie", "pepperoni", "hawaii"]

ALLOWED_DISHES = ["soup", "pizza", "hamburger", "kebab", "sushi", "cola"]


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(
                text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(
            text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
            return {"pizza_type": None}
        dispatcher.utter_message(
            text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}


class ShowTime(Action):
    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")
        return []


class ValidateBookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_restaurant_booking_form"

    def validate_dishes(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        # if slot_value.lower() not in ALLOWED_DISHES:
        #     dispatcher.utter_message(
        #         text=f"I don't recognize that dishes. We serve {'/'.join(ALLOWED_DISHES)}.")
        #     return {"dishes": None}
        if slot_value:
            # for i, dish in slot_value:
            #     dispatcher.utter_message(text=f"Dish {i}: {dish}")

            dispatcher.utter_message(text=f"Dishes: {slot_value}")
                # text=f"OK! You want to have a {slot_value} dishes.")
            return {"dishes": slot_value}
        else:
            dispatcher.utter_message(text="Upss... can you repeat?")
            return {'dishes': None}

    def validate_num_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if int(slot_value) >= 20:
            dispatcher.utter_message(
                text=f"I don't understand. can you choose number from 1 to 6?")
            return {"num_people": None}
        dispatcher.utter_message(
            text=f"OK! You want table for {slot_value} people.")
        return {"num_people": slot_value}

class SubmitBookingForm(Action):
    def name(self) -> Text:
        return "submit_booking_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        table_type = ''
        if tracker.get_slot('outdoor_seating'): table_type = 'outdoor'
        else: table_type = 'indoor'

        dispatcher.utter_message(
            text=f"OK! You want {table_type} table for {tracker.get_slot('num_people')} people.")

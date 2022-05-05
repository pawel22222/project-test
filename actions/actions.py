import types
from typing import Text, List, Any, Dict
import datetime as dt

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_DISHES = ["soup", "pizza", "hamburger", "kebab", "sushi", "cola"]

class ShowTime(Action):
    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")
        return []


class ValidateBookingTableForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_table_form"

    def validate_dishes(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        for dish in slot_value:
            if dish.lower() not in ALLOWED_DISHES:
                dispatcher.utter_message(
                text=f"I don't recognize that dishes. We serve {'/'.join(ALLOWED_DISHES)}.")
                return {"dishes": None}

        dispatcher.utter_message(text=f"Dishes: {slot_value}")
        return {"dishes": slot_value}


    def validate_num_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if int(slot_value) <= 15:
            dispatcher.utter_message(text=f"OK! You want table for {slot_value} people.")
            return {"num_people": slot_value}
        else:
            dispatcher.utter_message(text=f"I don't understand. can you choose number from 1 to 15?")
            return {"num_people": None}
    

    def validate_outdoor_seating(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        if isinstance(slot_value, types.BooleanType):
            return {"outdoor_seating": slot_value}
        else:
            return {"outdoor_seating": None}


class SubmitBookingTableForm(Action):
    def name(self) -> Text:
        return "submit_booking_table_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        table_type = ''
        if tracker.get_slot('outdoor_seating'): table_type = 'outdoor'
        else: table_type = 'indoor'

        dishes = ', '.join(tracker.get_slot('dishes'))

        dispatcher.utter_message(
            text=f"OK! You want {table_type} table for {tracker.get_slot('num_people')} people and you ordered {dishes}")


class DisplayTriggerButtons(Action):
    def name(self) -> Text:
        return "display_trigger_buttons"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ):
        task = tracker.get_slot("task")
        reason = tracker.get_slot("reason")

        def get_buttons():
            if task == 'hall_renting':
                return [
                    {"payload": "/prices", "title": f"price of {reason}"},
                    {"payload": "/available_dates", "title": f"{reason} dates available"},
                ]

            if task == 'cancellation_hall_renting':
                return [
                    {"payload": "/prices", "title": "cancellation costs"},
                    {"payload": "/time_to_cancel", "title": "time to cancel"}
                ]
                
            if task == 'daily_catering':
                return [
                    {"payload": "/prices", "title": f"price of {reason} catering"},
                    {"payload": "/delivery", "title": "delivery"},
                    {"payload": "/meals", "title": f"{reason} meals"}
                ]


        dispatcher.utter_message(
            text="what do you want to know?",
            buttons=get_buttons()
        )

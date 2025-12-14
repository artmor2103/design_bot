from aiogram.fsm.state import State, StatesGroup


class RegExample(StatesGroup):
    name = State()
    number = State()
    location = State()


class AIFlow(StatesGroup):
    waiting_for_prompt = State()

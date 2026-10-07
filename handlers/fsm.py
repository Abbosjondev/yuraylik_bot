from aiogram.fsm.state import State, StatesGroup

class AddRecordFSM(StatesGroup):
    wait_for_minutes = State()
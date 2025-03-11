from aiogram.fsm.state import State, StatesGroup

class UserInputHandler(StatesGroup):
    waiting_for_input = State()  # Ожидание ввода новой задачи
    waiting_for_edit = State()   # Ожидание редактирования задачи
    waiting_for_subtask = State()  # Ожидание добавления подзадачи
    waiting_for_deadline = State()  # Ожидание добавления дедлайна

    waiting_for_enter = State()
    waiting_for_reg = State()
    waiting_for_enter_password = State()
    waiting_for_reg_password = State()

    waiting_for_code = State()
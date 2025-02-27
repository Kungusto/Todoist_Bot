from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

class UserInputHandler(StatesGroup):
    waiting_for_input = State()  # Ожидание ввода новой задачи
    waiting_for_edit = State()   # Ожидание редактирования задачи
    waiting_for_subtask = State()  # Ожидание добавления подзадачи

    @staticmethod
    async def get_user_input(message: Message, state: FSMContext, prompt: str, parse_mode: str):
        """Запрашивает ввод от пользователя и переводит FSM в состояние ожидания."""
        await state.set_state(UserInputHandler.waiting_for_input)
        await message.answer(prompt, parse_mode=parse_mode)

    @staticmethod
    async def get_edit_input(message: Message, state: FSMContext, prompt: str, parse_mode: str):
        """Запрашивает ввод от пользователя для редактирования задачи."""
        await state.set_state(UserInputHandler.waiting_for_edit)
        await message.answer(prompt, parse_mode=parse_mode)

    @staticmethod
    async def get_edit_subtask(message: Message, state: FSMContext, prompt: str, parse_mode: str):
        """Запрашивает ввод от пользователя для редактирования задачи."""
        await state.set_state(UserInputHandler.waiting_for_edit)
        await message.answer(prompt, parse_mode=parse_mode)

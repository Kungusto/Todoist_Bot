﻿from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

class UserInputHandler(StatesGroup):
    waiting_for_input = State()  # Ожидание ввода новой задачи
    waiting_for_edit = State()   # Ожидание редактирования задачи

    @staticmethod
    async def get_user_input(message: Message, state: FSMContext, prompt: str):
        """Запрашивает ввод от пользователя и переводит FSM в состояние ожидания."""
        await state.set_state(UserInputHandler.waiting_for_input)
        await message.answer(prompt)

    @staticmethod
    async def get_edit_input(message: Message, state: FSMContext, prompt: str):
        """Запрашивает ввод от пользователя для редактирования задачи."""
        await state.set_state(UserInputHandler.waiting_for_edit)
        await message.answer(prompt)

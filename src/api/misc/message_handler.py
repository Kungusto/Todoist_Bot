from aiogram import Router, types, F
from src.api.ai import AI
import re

router = Router()

# Обработчик для сообщений, содержащих "банан" с учётом регистра и возможного пробела
@router.message(F.text.regexp(r'\bбанан\b\s*', flags=re.IGNORECASE))
async def banana_handler(message: types.Message):
    await message.answer_photo(
        photo="https://drive.google.com/uc?id=1XIPisEyTKyUwYB_5gj8C61SEoO-CLb1O",  # Прямая ссылка на изображение
        caption="🍌 Пасхалочка!"
    )

# Обработчик для всех других сообщений
@router.message(F.text.regexp(r'.*', flags=re.IGNORECASE))
async def other_message_handler(message: types.Message):
    ai = AI(message.text)
    answer = await ai.handle_other_message()
    await message.answer(answer, parse_mode="HTML")

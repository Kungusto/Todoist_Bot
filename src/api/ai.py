import asyncio
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
import torch
from datetime import datetime, timedelta
import ssl
from deep_translator import GoogleTranslator

ssl._create_default_https_context = ssl._create_unverified_context

# Загружаем модель и токенизатор
model_name = "Jean-Baptiste/camembert-ner-with-dates"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name).to(device)

# Создаём пайплайн для распознавания дат
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


class AI:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def translate_to_french(self, text: str) -> str:
        """Переводит русский текст на французский с исправлением ошибок."""
        translation = GoogleTranslator(source="ru", target="fr").translate(text)
        # Исправляем возможные ошибки перевода
        translation = translation.replace("APRONS", "Dans")  # Исправляем неверный перевод
        return translation

    def get_current_date(self):
        """Получает текущую дату."""
        return datetime.now()

    def parse_relative_date(self, text):
        """Обрабатывает относительные даты и возвращает дату в будущем."""
        units = {
            "JOUR": "days",
            "JOURS": "days",
            "HEURE": "hours",
            "HEURES": "hours",
            "MINUTE": "minutes",
            "MINUTES": "minutes"
        }

        current_date = self.get_current_date()
        delta = timedelta()

        words = text.split()
        for i in range(len(words) - 1):
            try:
                value = int(words[i])
                unit = words[i + 1].upper()
                if unit in units:
                    delta += timedelta(**{units[unit]: value})
            except ValueError:
                continue

        return (current_date + delta).strftime("%Y-%m-%d %H:%M")

    async def get_data(self):
        """Определяет новую дату, добавляя интервал ко времени."""
        print("Формируем дату")

        # Переводим запрос
        translated_prompt = self.translate_to_french(self.prompt)
        print("Переведённый запрос:", translated_prompt)

        # Извлекаем даты из текста
        extracted_dates = ner_pipeline(translated_prompt)
        print("Извлечённые данные:", extracted_dates)

        for entity in extracted_dates:
            if entity["entity_group"] == "DATE":
                date_text = entity["word"]

                # Если дата в формате относительного времени, конвертируем её
                if any(word in date_text.upper() for word in ["JOUR", "JOURS", "HEURE", "HEURES", "MINUTE", "MINUTES"]):
                    return self.parse_relative_date(date_text)

                # Если дата абсолютная, пробуем парсить её
                try:
                    parsed_date = datetime.strptime(date_text, "%d %B %Y")
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    pass

        print("Ошибка: не удалось распознать дату")
        return "-10"


ai = AI("Через 1 день и 2 часа")
result = asyncio.run(ai.get_data())
print("Результат:", result)

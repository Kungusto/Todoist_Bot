from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datetime import datetime

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="cpu")
tokenizer = AutoTokenizer.from_pretrained(model_name)

class AI:
    def __init__(self, prompt:str):
        self.prompt = prompt

    def get_tomorrow_date(self):
        """Вычисляет сегодняшнюю дату."""
        today = datetime.now()
        return today.strftime("%Y-%m-%d-%H-%M")  # Фикс: теперь возвращает строку


    def get_data(self):
        """Форматирует дату через нейросеть (если нужно изменить формат)."""
        data = self.get_tomorrow_date()  # Получаем дату как строку
        prompt = self.prompt
        prompt = f"Сейчас {data}, выведи новую дату с условием что {prompt}, выведи только дату в формате %Y-%m-%d-%H-%M."

        # Создаем входной текст
        messages = [
            {"role": "system", "content": "Ты — нейросеть, отвечай ТОЛЬКО датой в формате %Y:%m:%d:%H:%M используя только цифры и символ :, не используй символ -."},
            {"role": "user", "content": prompt}
        ]

        formatted_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(formatted_text, return_tensors="pt").to(model.device)

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=20, do_sample=False, temperature=None, top_p=None, top_k=None)

        # Декодируем текст и оставляем только последнее предложение (ответ модели)
        response = tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # Отделяем ответ модели от промпта
        response_lines = response.split("\n")  # Разбиваем на строки
        last_line = response_lines[-1].strip()  # Берем последнюю строку (ответ)

        return last_line
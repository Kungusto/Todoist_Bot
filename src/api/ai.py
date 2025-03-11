import asyncio
import ollama
from datetime import datetime
class AI:
    def __init__(self, prompt: str):
        self.prompt = prompt

    async def get_today_data(self):
        today = datetime.today()
        return today.strftime("%Y-%m-%d-%H-%M")

    async def get_data(self):
        """Определяет новую дату, отправляя запрос в Ollama."""
        print("Формируем дату...")

        # Явно указываем адрес Ollama
        client = ollama.Client(host="http://localhost:11434")
        today_data = await self.get_today_data()

        print(today_data)

        response = client.chat(model="qwen2.5-coder:latest", messages=[
            {"role": "system", "content": "Ты нейросеть, которая отвечает только датой в формате YYYY-mm-DD-HH-MM."
                                          "Учитывай, что если например сейчас 8 часов 10 июля и user пишет завтра, тебе надо просто прибавить день, а часы и минуты оставить те же, то есть ответ будет 2025-07-10-08-00."
                                          "Если текст user не имеет отношения к дате и времени выведи None."
                                          "Если дата или число которые пишет user меньше чем сегодняшняя пиши None."},
            {"role": "user", "content": f"Сегодня {today_data}. Какая дата и время будет {self.prompt}?"}
        ])

        answer = response["message"]["content"]

        if answer == "None": return None
        else: return answer
import asyncio
import json
import ollama
from datetime import datetime, timedelta
import re
class AI:
    def __init__(self, prompt: str):
        self.prompt = prompt

    async def get_today_data(self):
        today = datetime.today()
        return today.strftime("%Y-%m-%d-%H-%M-%S")

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

    async def get_task(self):
        """Определяет новую задачу, отправляя запрос в Ollama с данными о текущих задачах."""
        print("Формируем новую задачу...")
        from src.api import setup

        today_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Подготавливаем JSON-структуру задач для передачи нейросети
        tasks_data = [
            {
                "title": task[0],
                "subtasks": task[1],
                "priority": task[2],
                "status": task[3],
                "deadline": task[4]
            }
            for task in setup.task_buttons
        ]

        # Формируем сообщение для Ollama
        messages = [
            {"role": "system", "content":
                "Ты создаешь новую задачу, связанную с запросом пользователя. Ответ давай только в формате JSON.\n"
                "Формат: {'title': 'Название задачи', 'subtasks': ['Подзадача 1', 'Подзадача 2'], "
                "'priority': 2, 'status': 1, 'deadline': 'YYYY-MM-DD-HH-MM-SS'}.\n"
                "Приоритет: 1 - высокий, 2 - средний, 3 - низкий.\n"
                "Если в запросе пользователя есть слова 'не срочно', 'можно потом', 'когда будет время' – ставь приоритет 1.\n"
                "Если задача содержит несколько этапов, ставь **логичный порядок выполнения** в подзадачах."
             },
            {"role": "user", "content":
                f"Сейчас {today_date}. У меня есть такие задачи:\n"
                f"{json.dumps(tasks_data, ensure_ascii=False, indent=2)}\n"
                f"Создай новую задачу, связанную с \"{self.prompt}\"."
             }
        ]

        # Отправляем запрос в Ollama
        client = ollama.Client(host="http://localhost:11434")
        response = client.chat(model="qwen2.5-coder:latest", messages=messages)

        # Получаем ответ и ищем JSON внутри
        answer = response["message"]["content"]
        json_match = re.search(r'\{.*\}', answer, re.DOTALL)

        if not json_match:
            print("Ошибка: Ollama не вернула JSON", answer)
            return None

        try:
            new_task = json.loads(json_match.group())
            required_keys = ["title", "priority", "status", "deadline"]

            if all(key in new_task for key in required_keys):
                if new_task["deadline"]:
                    try:
                        task_deadline = datetime.strptime(new_task["deadline"], "%Y-%m-%d-%H-%M-%S")
                        if task_deadline < datetime.today():
                            print(f"⚠️ Дедлайн {new_task['deadline']} устарел. Устанавливаем новую дату...")
                            new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M-%S")
                    except ValueError:
                        print(f"Ошибка: некорректный формат даты {new_task['deadline']}. Устанавливаем новую дату...")
                        new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M-%S")
                else:
                    print("Ошибка: дедлайн отсутствует. Устанавливаем стандартное значение.")
                    new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M-%S")

                setup.task_buttons.append([
                    new_task["title"],
                    new_task.get("subtasks", []),
                    new_task["priority"],
                    new_task["status"],
                    new_task["deadline"]
                ])
                print("✅ Новая задача добавлена:", new_task)
                return new_task
            else:
                print("Ошибка: JSON не содержит все нужные ключи", new_task)
                return None
        except json.JSONDecodeError:
            print("Ошибка: Ollama вернула некорректный JSON", answer)
            return None

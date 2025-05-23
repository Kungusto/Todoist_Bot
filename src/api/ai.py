﻿import asyncio
import json
import ollama
from datetime import datetime, timedelta
import re
from src.utils.timezone_utils import get_user_timezone, get_format_deadline

class AI:
    def __init__(self, prompt: str):
        self.prompt = prompt

    async def get_today_data(self):
        """Возвращает сегодняшнюю дату и время с учётом часового пояса пользователя."""
        user_tz = await get_user_timezone()  # Получаем часовой пояс пользователя
        today = datetime.now(user_tz)  # Используем текущее время в этом часовом поясе
        print(today)
        return today.strftime("%Y-%m-%d-%H-%M")

    async def get_data(self):
        """Определяет новую дату, отправляя запрос в Ollama."""
        print("Формируем дату...")

        # Явно указываем адрес Ollama
        client = ollama.Client(host="http://ollama-server:11434")
        today_data = await self.get_today_data()


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

        today_date = datetime.now().strftime("%Y-%m-%d-%H-%M")

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
                "Если в задаче есть лишние слова то в название задачи оставляй только заголовок."
                "Если задача содержит несколько этапов, ставь **логичный порядок выполнения** в подзадачах."
             },
            {"role": "user", "content":
                f"Сейчас {today_date}. У меня есть такие задачи:\n"
                f"{json.dumps(tasks_data, ensure_ascii=False, indent=2)}\n"
                f"Создай новую задачу, связанную с \"{self.prompt}\"."
             }
        ]

        # Отправляем запрос в Ollama
        client = ollama.Client(host="http://ollama-server:11434")
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
                        task_deadline = datetime.strptime(new_task["deadline"], "%Y-%m-%d-%H-%M")
                        if task_deadline < datetime.today():
                            print(f"⚠️ Дедлайн {new_task['deadline']} устарел. Устанавливаем новую дату...")
                            new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M")
                    except ValueError:
                        print(f"Ошибка: некорректный формат даты {new_task['deadline']}. Устанавливаем новую дату...")
                        new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M")
                else:
                    print("Ошибка: дедлайн отсутствует. Устанавливаем стандартное значение.")
                    new_task["deadline"] = (datetime.today() + timedelta(days=3)).strftime("%Y-%m-%d-%H-%M")
                    # Если deadline в строковом формате, преобразуем в datetime перед вызовом get_format_deadline
                if isinstance(new_task["deadline"], str):
                    task_deadline = datetime.strptime(new_task["deadline"], "%Y-%m-%d-%H-%M")
                else:
                    task_deadline = new_task["deadline"]

                deadline = get_format_deadline(task_deadline)
                setup.task_buttons.append([
                    new_task["title"],
                    new_task.get("subtasks", []),
                    new_task["priority"],
                    1,
                    deadline
                ])
                print("✅ Новая задача добавлена:", new_task)
                return new_task
            else:
                print("Ошибка: JSON не содержит все нужные ключи", new_task)
                return None
        except json.JSONDecodeError:
            print("Ошибка: Ollama вернула некорректный JSON", answer)
            return None

    async def handle_other_message(self):
        """Обрабатывает остальные сообщения, отправляя запрос нейросети."""
        print("Обрабатываем сообщение...")

        from src.api import setup

        # Формируем запрос для нейросети
        prompt = f"Пользователь написал: {self.prompt}. Сгенерируй на это сообщение разумный ответ."

        # Создаём клиент Ollama
        client = ollama.Client(host="http://ollama_server:11434")

        # Сообщение для нейросети
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты — встроенный помощник в Telegram-боте, который работает как аналог Todoist — приложения для управления задачами.\n"
                    "Отвечай от первого лица, дружелюбно и кратко. Не называй себя ИИ, нейросетью или моделью. Не выдумывай задачи, не создавай и не изменяй их самостоятельно — только по команде пользователя.\n\n"

                    "📌 Возможности бота:\n"
                    "• Создание задач и подзадач из обычного текста;\n"
                    "• Распознавание дедлайнов в формате 'завтра', 'через 3 дня', 'в пятницу';\n"
                    "• Установка приоритетов (1 — высокий, 2 — средний, 3 — низкий);\n"
                    "• Отображение, фильтрация и редактирование задач;\n"
                    "• Вся работа происходит через Telegram — задачи отображаются в виде кнопок, доступен просмотр подзадач, дедлайна и статуса.\n\n"

                    "💡 Примеры, как пользоваться:\n"
                    "— Напиши: <b>купить продукты завтра</b> — я предложу задачу с дедлайном;\n"
                    "— Напиши: <b>покажи задачи</b> или <b>что у меня на сегодня?</b> — я выведу активные задачи;\n"
                    "— Спроси: <b>что с задачей “отчёт”?</b> — я проверю её в списке;\n"
                    "— Напиши: <b>отфильтруй просроченные</b> — и я покажу только просроченные задачи.\n\n"

                    "🗂 Текущий список задач пользователя:\n"
                    f"{json.dumps([{'title': t[0], 'subtasks': t[1], 'priority': t[2], 'status': t[3], 'deadline': t[4]} for t in setup.task_buttons], ensure_ascii=False, indent=2)}\n\n"

                    "💬 Ты можешь задать любые вопросы, даже не связанные с задачами, например, попросить анекдот, сказку или просто поболтать.\n"
                    "Но не забывай, что я все же помощник по задачам и могу только предложить идеи для задач или помочь с их организацией.\n\n"

                    "⚠️ Ты не должен самостоятельно создавать, удалять или изменять задачи — только по просьбе пользователя."
                )
            },
            {
                "role": "user",
                "content": f"Пользователь написал: {self.prompt}. Сгенерируй на это разумный, лаконичный ответ, если можно — с уточнением по задачам."
            }
        ]

        # Отправляем запрос в Ollama
        response = client.chat(model="qwen2.5-coder:latest", messages=messages)
        answer = response["message"]["content"]

        # Печатаем и отправляем результат
        print(f"Ответ от нейросети: {answer}")

        # Отправляем ответ пользователю
        if answer:
            return answer
        else:
            return "Извините, я не смог понять ваш запрос."

# async def main():
#     ai = AI("Сходить к врачу завтра на машине")
#     await ai.get_data()
#
# if __name__ == "__main__":
#     asyncio.run(main())
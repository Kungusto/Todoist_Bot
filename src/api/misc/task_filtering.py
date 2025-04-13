from datetime import date
from typing import Callable

class Filter:
    def __init__(self):
        from src.api import setup
        from src.api.register import Register
        from src.api.misc.task_sorting import Sort

        self.settings = setup.settings

        sort = Sort()
        self.task_buttons = sort.get_sorted()

        # Регистрация фильтров по индексу
        self.filter_methods: dict[int, Callable[[], list]] = {
            0: self.get_active_tasks,
            1: self.get_completed_tasks,
            2: self.get_overdue_tasks,
            3: self.get_high_priority_tasks,
            4: self.get_today_tasks,
            5: self.get_all_tasks
        }

        self.register = Register()

    def get_active_tasks(self):
        return [task for task in self.task_buttons if task[3] in (1, 2)]

    def get_completed_tasks(self):
        return [task for task in self.task_buttons if task[3] == 4]

    def get_overdue_tasks(self):
        today = date.today().strftime("%Y-%m-%d")
        return [task for task in self.task_buttons if task[4][:10] < today]

    def get_high_priority_tasks(self):
        return [task for task in self.task_buttons if task[2] == 3]

    def get_today_tasks(self):
        today = date.today().strftime("%Y-%m-%d")
        return [task for task in self.task_buttons if task[4][:10] == today]

    def get_all_tasks(self):
        return self.task_buttons.copy()

    def get_filtered(self) -> list:
        self.register.register_task(self.filter_methods.get(self.settings.get("task_filter", 5), self.get_all_tasks)())
        return self.filter_methods.get(self.settings.get("task_filter", 5), self.get_all_tasks)()
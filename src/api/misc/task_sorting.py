from datetime import datetime
from typing import Callable

class Sort:
    def __init__(self):
        from src.api.setup import task_buttons, settings
        from src.api.register import Register
        self.task_buttons = task_buttons
        self.task_sort = settings["task_sort"]

        self.sorting_methods: dict[int, Callable[[], list]] = {
            0: self.original_order,
            1: self.by_date_asc,
            2: self.by_date_desc,
            3: self.by_priority,
            4: self.alphabetically
        }

        self.register = Register()

    def by_date_asc(self):
        return sorted(self.task_buttons, key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%H-%M-%S"))

    def by_date_desc(self):
        return sorted(self.task_buttons, key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%H-%M-%S"), reverse=True)

    def by_priority(self):
        return sorted(self.task_buttons, key=lambda x: x[2])

    def alphabetically(self):
        return sorted(self.task_buttons, key=lambda x: x[0].lower())

    def original_order(self):
        return self.task_buttons.copy()

    def get_sorted(self) -> list:
        self.register.register_task(self.sorting_methods.get(self.task_sort, self.original_order)())
        return self.sorting_methods.get(self.task_sort, self.original_order)()

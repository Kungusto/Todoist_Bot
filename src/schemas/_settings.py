from pydantic import BaseModel

class Setting(BaseModel):
    id: int
    user_id: int
    task_sort: int
    task_filter: int
    notifications: bool
    time_format: int
    auto_delete: int
    ai: bool
    language: str

class SettingAdd(BaseModel):
    user_id: int
    task_sort: int = 4
    task_filter: int = 5
    notifications: bool = False
    time_format: int = 24
    auto_delete: int = 7
    ai: bool = True
    language: str = "Russian"

class SettingEdit(BaseModel):
    task_sort: int | None = None
    task_filter: int | None = None
    notifications: bool | None = None
    time_format: int | None = None
    auto_delete: int | None = None
    ai: bool | None = None
    language: str | None = None

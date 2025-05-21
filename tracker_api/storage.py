from typing import Dict
from models.user_models import UserRead
from models.task_models import Task

USERS: Dict[int, UserRead] = {}
TASKS: Dict[int, Task] = {}
from fastapi import FastAPI, HTTPException
from models.user_models import UserCreate, UserRead
from models.task_models import Task
from storage import USERS, TASKS

app = FastAPI()
user_id_counter = 1
task_id_counter = 1

# ✅ Root Route
@app.get("/")
def root():
    return {"message": "✅ Task Tracker API is running!"}


# 👤 Create a User
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = UserRead(id=user_id_counter, **user.dict())
    USERS[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


# 👤 Get a User
@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 📝 Create a Task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    task.id = task_id_counter
    TASKS[task_id_counter] = task
    task_id_counter += 1
    return task


# 📝 Get a Task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# 🛠 Update Task Status
@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: int, status: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if status not in {"pending", "in_progress", "done"}:
        raise HTTPException(status_code=400, detail="Invalid status")
    task.status = status
    return task


# 📋 List all tasks for a user
@app.get("/users/{user_id}/tasks", response_model=list[Task])
def list_user_tasks(user_id: int):
    return [task for task in TASKS.values() if task.user_id == user_id]
from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).resolve().parent.parent / "data.db"

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            completed INTEGER NOT NULL DEFAULT 0,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
    yield

app = FastAPI(title="Users & Tasks API", version="1.0.0", lifespan=lifespan)

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=120)

class UserOut(UserCreate):
    id: int

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=500)
    user_id: int

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    try:
        with connect() as db:
            cur = db.execute("INSERT INTO users(name,email) VALUES (?,?)",
                             (payload.name, payload.email))
            row = db.execute("SELECT id,name,email FROM users WHERE id=?",
                             (cur.lastrowid,)).fetchone()
            return dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists")

@app.get("/users", response_model=list[UserOut])
def list_users():
    with connect() as db:
        return [dict(r) for r in db.execute(
            "SELECT id,name,email FROM users ORDER BY id").fetchall()]

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    with connect() as db:
        row = db.execute("SELECT id,name,email FROM users WHERE id=?",
                         (user_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with connect() as db:
        cur = db.execute("DELETE FROM users WHERE id=?", (user_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    with connect() as db:
        user = db.execute("SELECT id FROM users WHERE id=?", (payload.user_id,)).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        cur = db.execute(
            "INSERT INTO tasks(title,description,user_id) VALUES (?,?,?)",
            (payload.title, payload.description, payload.user_id))
        row = db.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone()
        return {**dict(row), "completed": bool(row["completed"])}

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(user_id: int | None = None):
    query = "SELECT * FROM tasks"
    params = ()
    if user_id is not None:
        query += " WHERE user_id=?"
        params = (user_id,)
    query += " ORDER BY id"
    with connect() as db:
        rows = db.execute(query, params).fetchall()
    return [{**dict(r), "completed": bool(r["completed"])} for r in rows]

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate):
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields supplied")
    if "completed" in changes and changes["completed"] is not None:
        changes["completed"] = int(changes["completed"])
    with connect() as db:
        current = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if current is None:
            raise HTTPException(status_code=404, detail="Task not found")
        assignments = ", ".join(f"{key}=?" for key in changes)
        db.execute(f"UPDATE tasks SET {assignments} WHERE id=?",
                   (*changes.values(), task_id))
        row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return {**dict(row), "completed": bool(row["completed"])}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with connect() as db:
        cur = db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")

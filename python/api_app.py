from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://slae-example-skit-vercel-python.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from random import choice


@app.get("/api/ping")
async def ping():
    return {"ping": choice(["pong!", "pong"])}


from python.todos import TodoSchema
from typing import List


@app.get("/api/getTodos", response_model=List[TodoSchema])
async def getTodos():
    return [
        TodoSchema(id=0, text="Store these somewhere other than runtime memory!"),
        TodoSchema(id=1, text="Do the dishes"),
    ]


@app.post("/api/completeTodo", response_model=TodoSchema)
async def completeTodo(payload: TodoSchema):
    return TodoSchema(id=payload.id, text=payload.text, completed=True)


@app.delete("/api/deleteTodo")
async def deleteTodo(payload: TodoSchema):
    return

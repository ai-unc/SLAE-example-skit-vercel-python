from pydantic import BaseModel, Field


class TodoSchema(BaseModel):
    id: int = Field(gt=-1)
    text: str = Field(..., min_length=3, max_length=50)
    completed: bool = False

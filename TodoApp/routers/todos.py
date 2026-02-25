from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import  SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0)
    complete: bool

@router.get("/")
def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def get_data_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

@router.post("/todos_add", status_code=status.HTTP_201_CREATED)
def add_data(user: user_dependency, db: db_dependency, todos_request: TodoRequest):
    todo_model = Todos(**todos_request.dict(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

@router.put("/todos_update/{todo_id}")
def update_date(db: db_dependency, update_request: TodoRequest, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="data not found")

    todo_model.title = update_request.title
    todo_model.description = update_request.description
    todo_model.priority = update_request.priority
    todo_model.complete = update_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo_delete/{todo_id}")
def delete_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    db.delete(todo_model)
    db.commit()

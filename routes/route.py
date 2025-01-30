from fastapi import APIRouter, HTTPException
from models.todos import Todo
from database.database import collection_name
from schemas.schemas import list_serial, individual_serial
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos

@router.get("/{id}")
async def get_todo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    todo = collection_name.find_one({"_id": ObjectId(id)})
    if todo:
        return individual_serial(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/")
async def create_todo(todo: Todo):
    collection_name.insert_one(todo.dict())
    return {"message": "Todo created successfully"}

@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    collection_name.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": todo.dict()}
    )
    return {"message": "Todo updated successfully"}

@router.delete("/{id}")
async def delete_todo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Todo deleted successfully"}
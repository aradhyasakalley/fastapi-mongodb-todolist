from fastapi import APIRouter, Depends, HTTPException, status
from models.todos import Todo
from models.user import User
from config.database import user_collection, collection_name
from schema.schemas import list_serial
from bson import ObjectId
import bcrypt

router = APIRouter()


# Mock authentication function
async def authenticate_user(username: str, password: str):
    user_data = user_collection.find_one({"username": username})
    if user_data:
        hashed_password = user_data.get("password", "")
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_data = user.dict()
    user_data['password'] = hashed_password
    user_collection.insert_one(user_data)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: User):
    if await authenticate_user(user.username, user.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

@router.get("/")
async def get_todos():
    todos = list_serial(collection_name.find())
    return todos

@router.post("/")
async def post_todo(todo:Todo):
    collection_name.insert_one(dict(todo))
    
@router.put("/{id}")
async def put_todo(id:str,todo:Todo):
    collection_name.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(todo)})
    
@router.delete("/{id}")
async def delete_todo(id:str):
    collection_name.find_one_and_delete({"_id":ObjectId(id)})
from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_all_messages() -> dict:
    return users

@app.post("/user/{user_name}/{age}")
async def create_message(user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Oleg")],
        age: int = Path(ge=18, le=120, description="Enter age", example=55)) -> dict:
    current_index = str(int(max(users, key=int)) + 1)
    mess = f"Имя: {user_name}, возраст: {age}"
    users[current_index] = mess
    return {"message": f"User {current_index} is registered"}

@app.put("/user/{user_id}/{user_name}/{age}")
async def update_message(user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Oleg")],
        age: int = Path(ge=18, le=120, description="Enter age", example=55),
        user_id: int = Path(ge=0)) -> dict:
    users[user_id] = f"Имя: {user_name}, возраст: {age}"
    return {"message": f"The user {user_id} is updated"}


@app.delete("/user/{user_id}")
async def delete_user(user_id: str = Path(...)):
    if user_id in users:
        users.pop(user_id)
        return {"message": f"Пользователь с ID {user_id} удален."}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

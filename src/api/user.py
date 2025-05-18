from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from datetime import datetime
from src.api import auth

from src.api.models import User

router = APIRouter(
    prefix="/user", 
    tags=["User"],
    dependencies=[Depends(auth.get_api_key)],)



@router.get("/get/by_id/{user_id}", response_model=User)
def get_user(user_id: int):
    """
    Get User by ID.
    """
    # Placeholder for actual database call
    with db.engine.begin() as connection:
        user = connection.execute(
            sqlalchemy.text("""
                SELECT *
                FROM "user"
                WHERE id = :user_id
            """),
            {
             "user_id": user_id,
             },
        ).one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/get/by_name/{username}", response_model=User)
def get_user_by_name(username: str):
    """
    Get User by name.
    """
    # Placeholder for actual database call
    with db.engine.begin() as connection:
        user = connection.execute(
            sqlalchemy.text("""
                SELECT *
                FROM "user"
                WHERE name = :username
            """),
            {
             "username": username,
             },
        ).one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/make", response_model=User)
def make_user(name: str):
    """
    Make a new user.
    """
    # Placeholder for actual database call
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    # Save the user to the database
    with db.engine.begin() as connection:
        user_id = connection.execute(
            sqlalchemy.text("""
                INSERT INTO "user" (name)
                VALUES (:name)
                RETURNING id
            """),
            {
             "name": name,
             },
        ).scalar_one()
    
    new_user = User(
        id = user_id,
        name = name
    )

    return new_user
    
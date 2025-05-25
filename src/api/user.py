import re
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

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")



@router.get("/by_id/{user_id}", response_model=User)
def get_user(user_id: int):
    """
    Get User by ID.
    """
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
        ).scalar_one_or_none()
    
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")

        return user

@router.get("/by_name/{username}", response_model=User)
def get_user_by_name(username: str):
    """
    Get User by name.
    """
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
        ).scalar_one_or_none()
    
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with name={username} not found")
        return user

@router.post("/make", response_model=User)
def make_user(name: str):
    """
    Make a new user.
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    if not USERNAME_REGEX.fullmatch(name):
        raise HTTPException(
            status_code=400,
            detail="Username must only contain letters, numbers, dashes, or underscores"
        )
    
    # Save the user to the database
    with db.engine.begin() as connection:
        
        # Check if the user already exists
        existing_user = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM "user"
                WHERE name = :name
            """),
            {
             "name": name,
             },
        ).scalar_one_or_none()
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with name '{name}' already exists"
            )
    
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
    
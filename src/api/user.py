import re
from fastapi import APIRouter, HTTPException, status, Depends
import sqlalchemy
from src import database as db
from src.api import auth

from src.api.models import User, User_Favorites
from src.api.character import get_character_by_id
from src.api.franchise import get_franchise_by_id


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
        ).one_or_none()
    
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
        ).one_or_none()
    
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
    

@router.post("/favorite/character")
def set_favorite_character(user_id: int, char_id: int):
    """
    Sets a user's favorite character.
    """

    #Checks to see if the user and character exist, should error if they dont
    get_user(user_id)
    get_character_by_id(char_id) 

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                UPDATE "user"
                SET fav_char_id = :char_id
                WHERE id = :user_id
            """), 
            {
                "char_id": char_id,
                "user_id": user_id
            }
        )

    return {"message": "Favorite character was set"}


@router.post("/favorite/franchise")
def set_favorite_franchise(user_id: int, fran_id: int):
    """
    Sets a user's favorite franchise.
    """

    #Also checks like the previous
    get_user(user_id)
    get_franchise_by_id(fran_id)

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                UPDATE "user"
                SET fav_fran_id = :fran_id
                WHERE id = :user_id
            """),
            {
                "fran_id": fran_id,
                "user_id": user_id
            }
        )

    return {"message": "Favorite franchise was set"}


@router.get("/favorite/character", response_model=User_Favorites)
def get_favorites(user_id: int):
    """
    Gets a user's favorite character and franchise.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("""
                SELECT fav_char_id, fav_fran_id
                FROM "user"
                WHERE id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).first()

        if not result:
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")

        return User_Favorites(
            favorite_character_id=result.fav_char_id,
            favorite_franchise_id=result.fav_fran_id
        )

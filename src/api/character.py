from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db

from src.api.models import Character, CharacterMakeResponse, Franchise, FranchiseCharacterAssignment, Returned_Review, ReturnedCharacter
from src.api import auth

router = APIRouter(
    prefix="/character", 
    tags=["Character"],
    dependencies=[Depends(auth.get_api_key)],)



@router.get("/get/by_id/{character_id}", response_model=ReturnedCharacter)
def get_character_by_id(character_id: int):
    """
    Get character by ID.
    """
    
    with db.engine.begin() as connection:
        character = connection.execute(
            sqlalchemy.text("""
                SELECT id, user_id, name, description, rating, strength, speed, health
                FROM character
                WHERE id = :id
            """),
            {
                "id": character_id
            }
        ).one()
    
    the_character = ReturnedCharacter(
        char_id=character_id,
        user_id=character.user_id,
        name=character.name,
        description=character.description,
        rating=character.rating,
        strength=character.strength,
        speed=character.speed,
        health=character.health,
    )

    return the_character


@router.get("/list/{user_id}", response_model=list[ReturnedCharacter])
def get_user_characters(user_id: int):
    """
    Get all characters made by user.
    """

    with db.engine.begin() as connection:
        characters = connection.execute(
            sqlalchemy.text("""
                SELECT id, user_id, name, description, rating, strength, speed, health
                FROM character
                WHERE user_id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).all()
    
    user_characters = [
        ReturnedCharacter(
            char_id=character.id,
            user_id=character.user_id,
            name=character.name,
            description=character.description,
            rating=character.rating,
            strength=character.strength,
            speed=character.speed,
            health=character.health,
        )
        for character in characters
    ]
    return user_characters



@router.get("/get_review/{character_id}", response_model=list[Returned_Review])
def get_character_review(character_id: int):
    """
    Get all reviews for a given character referencing its id.
    """
    with db.engine.begin() as connection:
        comments = connection.execute(
            sqlalchemy.text("""
                SELECT user_id, comment
                FROM c_review
                WHERE char_id = :char_id
            """),
            {
                "char_id": character_id
            }
        ).all()

    all_comments = []
    for comment in comments:
        all_comments.append(
            Returned_Review(
                user_id = comment.user_id,
                comment = comment.comment
            )
        )

    return all_comments


@router.get("/leaderboard", response_model=list[CharacterMakeResponse])
def get_leaderboard():
    """
    Get the leaderboard of characters.
    """
    
    with db.engine.begin() as connection:
        characters = connection.execute(
            sqlalchemy.text("""
                SELECT id, user_id, name, description, rating, strength, speed, health
                FROM character
                ORDER BY rating DESC
                LIMIT 10
            """)
        ).all()
    
    characters = [ 
        ReturnedCharacter(
            char_id=character.id,
            user_id=character.user_id,
            name=character.name,
            description=character.description,
            rating=character.rating,
            strength=character.strength,
            speed=character.speed,
            health=character.health,
        )
        for character in characters
    ]
    
    return characters



@router.post("/make", response_model=CharacterMakeResponse)
def make_character(user_id: int, character: Character, franchiselist: list[FranchiseCharacterAssignment]):
    """
    Create a new character.
    """
    # Placeholder for actual database call
    
    with db.engine.begin() as connection:
        char_id = connection.execute(
            sqlalchemy.text("""
                INSERT INTO character (user_id, name, description, rating, strength, speed, health)
                VALUES (:user_id, :name, :description, :rating, :strength, :speed, :health)
                RETURNING id
            """),
            {
                "user_id": user_id,
                "name": character.name,
                "description": character.description,
                "rating": 0,
                "strength": character.strength,
                "speed": character.speed,
                "health": character.health,
            },
        ).scalar_one()
        # Assign character to franchises
        for franchise in franchiselist:
            #check if franchise exists
            franchise_id = connection.execute(
                sqlalchemy.text("""
                    SELECT id
                    FROM franchise
                    WHERE id = :franchise_id
                """),
                {
                    "franchise_id": franchise.franchise_id
                }
            ).scalar_one_or_none()
            
            if franchise_id is None:
                raise HTTPException(status_code=404, detail=f"Franchise id={franchise} not found")
            
            connection.execute(
                sqlalchemy.text("""
                    INSERT INTO char_fran (char_id, franchise_id)
                    VALUES (:char_id, :franchise_id)
                """),
                {
                    "char_id": char_id,
                    "franchise_id": franchise.franchise_id
                }
            )
            

    new_character = CharacterMakeResponse(
        char_id = char_id,
        user_id = user_id,
        name = character.name,
        description = character.description,
        rating = 0,
        strength = character.strength,
        speed = character.speed,
        health = character.health
    )

    return new_character

@router.get("/get/franchise/{character_id}", response_model=list[Franchise])
def get_character_franchises(char_id: int):
    """
    Get all franchises for a given character referencing its id.
    """
    with db.engine.begin() as connection:
        franchises = connection.execute(
            sqlalchemy.text("""
                SELECT f.name, f.description
                FROM franchise f
                JOIN char_fran cf ON f.id = cf.franchise_id
                WHERE cf.char_id = :char_id
            """),
            {
                "char_id": char_id
            }
        ).all()

    all_franchises = []
    for franchise in franchises:
        all_franchises.append(
            Franchise(
                name = franchise.name,
                description = franchise.description
            )
        )

    return all_franchises


@router.post("/review/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def review_character(user_id: int, character_id: int, comment: str):
    """
    Review a character.
    """
    if not comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                INSERT INTO c_review (user_id, char_id, comment)
                VALUES (:user_id, :char_id, :comment)
            """),
            {
                "user_id": user_id,
                "char_id": character_id,
                "comment": comment
            },
        )
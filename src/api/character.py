import re
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db

from src.api.models import Character, CharacterMakeResponse, Franchise, FranchiseCharacterAssignment, ReturnedCharacter
from src.api import auth

router = APIRouter(
    prefix="/character", 
    tags=["Character"],
    dependencies=[Depends(auth.get_api_key)],)

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")

@router.get("/by_id/{character_id}", response_model=ReturnedCharacter)
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
        ).scalar_one()
        
        if not character:
            raise HTTPException(status_code=404, detail=f"Character with id={character_id} not found")
        
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
        
        # If no characters are found, return an empty list
        if not characters:
            return []
    
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
        
        # If no characters are found, return an empty list
        if not characters:
            return []
    
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
    # Wall of Contraints on what a valid input is lol
    if not USERNAME_REGEX.fullmatch(character.name):
        raise HTTPException(status_code=400, detail="Character Name must only contain letters, numbers, dashes, or underscores")     
    if not character.name:
        raise HTTPException(status_code=400, detail="Character name cannot be empty")
    if not character.description:
        raise HTTPException(status_code=400, detail="Character description cannot be empty")
    if character.strength < 0:
        raise HTTPException(status_code=400, detail="Character strength cannot be negative")
    if character.speed < 0:
        raise HTTPException(status_code=400, detail="Character speed cannot be negative")
    if character.health < 0:
        raise HTTPException(status_code=400, detail="Character health cannot be negative")
    if not franchiselist:
        raise HTTPException(status_code=400, detail="Character must be assigned to at least one franchise")
    
    
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
            ).scalar_one()
            
            if not franchise_id:
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

@router.get("/franchise/{character_id}", response_model=list[Franchise])
def get_character_franchises(character_id: int):
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
                "char_id": character_id
            }
        ).all()
        
        if not franchises:
            raise HTTPException(status_code=404, detail="No franchises found for this character")

        all_franchises = []
        for franchise in franchises:
            all_franchises.append(
                Franchise(
                    name = franchise.name,
                    description = franchise.description
                )
            )

        return all_franchises



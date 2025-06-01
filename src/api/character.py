from fastapi import APIRouter, HTTPException, Depends
import sqlalchemy
from src import database as db

from src.api.models import Character, CharacterMakeResponse, FranchiseCharacterAssignment, FranchiseReturnResponse, ReturnedCharacter
from src.api import auth

router = APIRouter(
    prefix="/character", 
    tags=["Character"],
    dependencies=[Depends(auth.get_api_key)],)

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
        ).one_or_none()
        
        if character is None:
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


@router.get("/list/{user_id}/{page_number}", response_model=list[ReturnedCharacter])
def get_user_characters(user_id: int, page_number: int):
    """
    Get all characters made by user.
    """
    if page_number < 0:
        raise HTTPException(status_code=400, detail=f"Page Number must not be negative")
    
    with db.engine.begin() as connection:
        # Check if user exists
        user_exists = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM "user"
                WHERE id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).one_or_none()
        
        if user_exists is None:
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
        
        page_size = 10
        offset = page_number * page_size
        
        query = sqlalchemy.text(f"""
            SELECT id, user_id, name, description, rating, strength, speed, health
            FROM character
            WHERE user_id = :user_id
            LIMIT {page_size} OFFSET {offset}
        """)
        
        characters = connection.execute(query, {
            "user_id": user_id
        }).all()
        
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
    if not character.name:
        raise HTTPException(status_code=400, detail="Character name cannot be empty")
    if not character.description:
        raise HTTPException(status_code=400, detail="Character description cannot be empty")
    if character.strength <= 0:
        raise HTTPException(status_code=400, detail="Character strength cannot be negative or zero")
    if character.speed <= 0:
        raise HTTPException(status_code=400, detail="Character speed cannot be negative or zero")
    if character.health <= 0:
        raise HTTPException(status_code=400, detail="Character health cannot be negative or zero")
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
            ).one_or_none()
            
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

@router.get("/franchise/{character_id}/{page_number}", response_model=list[FranchiseReturnResponse])
def get_character_franchises(character_id: int, page_number: int):
    """
    Get all franchises for a given character referencing its id.
    """
    if page_number < 0:
        raise HTTPException(status_code=400, detail=f"Page Number must not be negative")
    
    with db.engine.begin() as connection:
        # Check if character exists
        character_exists = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM character
                WHERE id = :char_id
            """),
            {
                "char_id": character_id
            }
        ).one_or_none()
        
        if character_exists is None:
            raise HTTPException(status_code=404, detail=f"Character with id={character_id} not found")
        
        page_size = 10
        offset = page_number * page_size
        
        query = sqlalchemy.text(f"""
            SELECT f.id, f.name, f.description
            FROM franchise f
            JOIN char_fran cf ON f.id = cf.franchise_id
            WHERE cf.char_id = :char_id
            LIMIT {page_size} OFFSET {offset}
        """)
        
        franchises = connection.execute(query, {
            "char_id": character_id
        }).all()
        
        if not franchises:
            raise HTTPException(status_code=404, detail="No franchises found for this character")

        all_franchises = []
        for franchise in franchises:
            all_franchises.append(
                FranchiseReturnResponse(
                    id = franchise.id,
                    name = franchise.name,
                    description = franchise.description
                )
            )

        return all_franchises



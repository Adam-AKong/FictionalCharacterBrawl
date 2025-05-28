from datetime import timedelta, datetime
from math import pow
import random

import sqlalchemy
from fastapi import APIRouter, HTTPException, Depends

from src.api.models import Battle, BattleCreateResponse, BattleResult, BattleVoteResponse
from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/battle", 
    tags=["Battle"],
    dependencies=[Depends(auth.get_api_key)],
    )


def calculate_score(opposing_health: int, strength: int, speed: int, votes: int) -> float:
    """
    Calculate the score for a character based on its health, strength, speed, and votes.
    """
    # Calculate the winner based on the votes and character stats
    # Lowest score wins. Votes are multiplied by a modifier to reduce the score
    # More votes = lower score = more likely to win
    # Formula: score = (health / (strength * speed)) * (vote_modifier ^ votes)
    vote_modifier = 0.9
    return (opposing_health / (strength * speed)) * (pow(vote_modifier, votes))

def calculate_winner(connection, battle) -> int:
    """
    Calculate the winner of a battle based on the votes and character stats.
    """
    with db.engine.begin() as connection:
        character1 = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM character
                WHERE id = :id
                """
            ),
            [{"id": battle.char1_id}]
        ).one()

        character2 = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM character
                WHERE id = :id
                """
            ),
            [{"id": battle.char2_id}]
        ).one()
        

        character1_score = calculate_score(
            character2.health, 
            character1.strength, 
            character1.speed, 
            battle.vote1
        )
        character2_score = calculate_score(
            character1.health, 
            character2.strength, 
            character2.speed, 
            battle.vote2
        )

        if character1_score < character2_score:
            # Character 1 wins
            # Increase the rating of the winner
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE character
                    SET rating = rating + 1
                    WHERE id = :id
                    """
                ),
                [{"id": battle.char1_id}]
            )
            return battle.char1_id
        elif character1_score > character2_score:
            # Character 2 wins
            # Increase the rating of the winner
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE character
                    SET rating = rating + 1
                    WHERE id = :id
                    """
                ),
                [{"id": battle.char2_id}]
            )
            return battle.char2_id
        else:
            # It's a tie, randomize the winner
            winner_id = battle.char1_id if random.randint(0, 1) == 0 else battle.char2_id
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE character
                    SET rating = rating + 1
                    WHERE id = :id
                    """
                ),
                [{"id": winner_id}]
            )
            return winner_id
            
def update_winner(connection, battle):
    """
    Update the winner of a battle in the database.
    """
    winner = calculate_winner(connection, battle)
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE battle
                SET winner_id = :winner
                WHERE id = :id
                """
            ),
            [{"winner": winner, "id": battle.id}]
        )
        return winner

@router.get("/battle/{battle_id}", response_model=BattleResult)
def get_battle_result(battle_id: int):
    """
    Get the result of a battle by its ID.
    """
    with db.engine.begin() as connection:
        battle = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle_with_votes
                WHERE id = :id
                FOR UPDATE
                """
            ),
            [{"id": battle_id}]
        ).one_or_none()
        
        if battle is None:
            raise HTTPException(status_code=404, detail=f"Battle with id {battle_id} not found")
        
        if battle.end_date > datetime.now():
            return BattleResult(
                battle_id=battle.id,
                user_id=battle.user_id,
                char1_id=battle.char1_id,
                char2_id=battle.char2_id,
                vote1=battle.vote1,
                vote2=battle.vote2,
                winner_id=None,
                start=battle.start_date,
                end=battle.end_date,
                finished=False
            )
        
        if battle.winner_id is None:
            # Calculate the winner if not already set
            winner = update_winner(connection, battle)
            
            return BattleResult(
                battle_id=battle.id,
                user_id=battle.user_id,
                char1_id=battle.char1_id,
                char2_id=battle.char2_id,
                vote1=battle.vote1,
                vote2=battle.vote2,
                winner_id=winner,
                start=battle.start_date,
                end=battle.end_date,
                finished=True
            )
    
        return BattleResult(
            battle_id=battle.id,
            user_id=battle.user_id,
            char1_id=battle.char1_id,
            char2_id=battle.char2_id,
            vote1=battle.vote1,
            vote2=battle.vote2,
            winner_id=battle.winner_id,
            start=battle.start_date,
            end=battle.end_date,
            finished=True
        )

@router.get("/character/{character_id}", response_model=list[BattleResult])
def character_participation(character_id: int):
    """
    Get a list of battles a character has fought in.
    """
    battles = []
    with db.engine.begin() as connection:
        # Get all battles for the character
        battlelist = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle_with_votes
                WHERE char1_id = :character OR char2_id = :character
                """
            ),
            [{"character": character_id}]
        ).fetchall()
        
        # If no battles are found, return an empty list
        if not battlelist:
            return []
        
        for b in battlelist:
            if b.end_date > datetime.now():
                finished = False
            else:
                finished = True
            # Check if the winner is set
            if b.winner_id is None and finished:
                winner = update_winner(connection, b)
            
                battles.append(
                    BattleResult(
                        battle_id=b.id,
                        user_id=b.user_id,
                        char1_id=b.char1_id,
                        char2_id=b.char2_id,
                        vote1=b.vote1,
                        vote2=b.vote2,
                        winner_id=winner,
                        start=b.start_date,
                        end=b.end_date,
                        finished=finished
                    )
                )  
            elif b.winner_id is None and not finished:
               # If the battle is still active and the winner is not set, just append the battle result
                battles.append(
                    BattleResult(
                        battle_id=b.id,
                        user_id=b.user_id,
                        char1_id=b.char1_id,
                        char2_id=b.char2_id,
                        vote1=b.vote1,
                        vote2=b.vote2,
                        winner_id=None,
                        start=b.start_date,
                        end=b.end_date,
                        finished=finished
                    )
                )
            else:
                # If the winner is already set, just append the battle result
                battles.append(
                    BattleResult(
                        battle_id=b.id,
                        user_id=b.user_id,
                        char1_id=b.char1_id,
                        char2_id=b.char2_id,
                        vote1=b.vote1,
                        vote2=b.vote2,
                        winner_id=b.winner_id,
                        start=b.start_date,
                        end=b.end_date,
                        finished=finished
                    )
                )
    return battles
            

@router.get("/user/{user_id}", response_model=list[BattleResult])
def user_participation(user_id: int):
    """
    Get a list of battles a user has participated in.
    """
    battles = []
    with db.engine.begin() as connection:
        battlelist = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle_with_votes
                WHERE user_id = :user
                """
            ),
            [{"user": user_id}]
        ).all()
        # If no battles found, return an empty list
        if not battlelist:
            return []
        
        for b in battlelist:
            # Check if the battle has ended
            if b.end_date > datetime.now():
                finished = False
            else:
                finished = True
            # Check if the winner is set
            if b.winner_id is None:
                # Calculate the winner if not already set
                winner = update_winner(connection, b)
                
                # Append the battle result
                battles.append(
                    BattleResult(
                        battle_id=b.id,
                        user_id=b.user_id,
                        char1_id=b.char1_id,
                        char2_id=b.char2_id,
                        vote1=b.vote1,
                        vote2=b.vote2,
                        winner_id=winner,
                        start=b.start_date,
                        end=b.end_date,
                        finished=finished
                    )
                )
            else:
                # If the winner is already set, just append the battle result
                battles.append(
                    BattleResult(
                        battle_id=b.id,
                        user_id=b.user_id,
                        char1_id=b.char1_id,
                        char2_id=b.char2_id,
                        vote1=b.vote1,
                        vote2=b.vote2,
                        winner_id=b.winner_id,
                        start=b.start_date,
                        end=b.end_date,
                        finished=finished
                    )
                )
    return battles

@router.post("/vote/{user_id}/{battle_id}/{character_id}", response_model=BattleVoteResponse)
def battle_vote(user_id: int, battle_id: int, character_id: int):
    """
    Vote for a character during an active battle.
    """    
    with db.engine.begin() as connection:
        # Check if the user exists
        user_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM "user"
                WHERE id = :id
                """
            ),
            [{"id": user_id}]
        ).scalar_one_or_none()
        
        if user_exists is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        
        
        # Check if the battle exists
        battle = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle
                WHERE id = :id
                """
            ),
            [{"id": battle_id}]
        ).one_or_none()
        
        if battle is None:
            raise HTTPException(status_code=404, detail=f"Battle with id {battle_id} not found")
        
        # Check if the battle is still active
        if battle.end_date < datetime.now():
            raise HTTPException(status_code=400, detail=f"Battle with id {battle_id} has already ended")
        
        character_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT char1_id, char2_id
                FROM battle
                WHERE id = :id
                """
            ),
            [{"id": battle_id}]
        ).one()
    
        if character_ids.char1_id == character_id or character_ids.char2_id == character_id:
            # Check if the user has already voted
            existing_vote = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT *
                    FROM battle_votes
                    WHERE user_id = :user AND battle_id = :battle
                    """
                ),
                [{"user": user_id, "battle": battle_id}]
            ).one_or_none()
            
            if existing_vote is not None:
                raise HTTPException(status_code=400, detail=f"User {user_id} has already voted in battle {battle_id}")
            
            # Insert the vote into the database
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO battle_votes (battle_id, user_id, char_id)
                    VALUES (:battle, :user, :char_id)
                    """
                ),
                [{
                    "battle": battle_id,
                    "user": user_id,
                    "char_id": character_id}]
            )
        else:
            raise HTTPException(status_code=400, detail=f"Character with id {character_id} is not part of battle {battle_id}")
        
    return BattleVoteResponse(
        message=f"User {user_id} has successfully voted",
        battle_id=battle_id,
        char_id=character_id,
    )

@router.post("/make", response_model=BattleCreateResponse)
def create_battle(battle_data: Battle):
    """
    Create a battle between two characters and return its id.
    """
    # Assuming duration is in hours
    
    if battle_data.char1_id == battle_data.char2_id:
        raise HTTPException(status_code=400, detail="Cannot create a battle with the same character")
    if battle_data.char1_id is None:
        raise HTTPException(status_code=400, detail="Character 1 ID cannot be None")
    if battle_data.char2_id is None:
        raise HTTPException(status_code=400, detail="Character 2 ID cannot be None")
    if battle_data.duration < 0:
        raise HTTPException(status_code=400, detail="Battle duration must not be negative")
    if battle_data.user_id is None:
        raise HTTPException(status_code=400, detail="User ID cannot be None")
    
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=battle_data.duration)
    
    with db.engine.begin() as connection:
        
        # Check if the characters exist
        char1_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM character
                WHERE id = :id
                """
            ),
            [{"id": battle_data.char1_id}]
        ).scalar_one_or_none()
        
        char2_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM character
                WHERE id = :id
                """
            ),
            [{"id": battle_data.char2_id}]
        ).scalar_one_or_none()
        
        if char1_exists is None:
            raise HTTPException(status_code=404, detail=f"Character 1 with id {battle_data.char1_id} not found")
        if char2_exists is None:
            raise HTTPException(status_code=404, detail=f"Character 2 with id {battle_data.char2_id} not found")
        
        battle_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO battle (user_id, char1_id, char2_id, start_date, end_date)
                VALUES (:user, :char1, :char2, :start, :end)
                RETURNING id
                """
            ),
            [{"user": battle_data.user_id,
              "char1": battle_data.char1_id,
              "char2": battle_data.char2_id,
              "start": start_time,
              "end": end_time
              }]
        ).scalar_one()
        
    return BattleCreateResponse(
        battle_id=battle_id,
        char1_id=battle_data.char1_id,
        char2_id=battle_data.char2_id,
        duration=battle_data.duration,
        start=start_time,
        end=end_time
    )
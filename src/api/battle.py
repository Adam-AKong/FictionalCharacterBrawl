from datetime import timedelta, datetime
from math import pow

import sqlalchemy
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import DateTime

from src.api.models import Battle, BattleCreateResponse, BattleResult, Character
from src import database as db
from src.api import auth

router = APIRouter(
    prefix="/battle", 
    tags=["Battle"],
    dependencies=[Depends(auth.get_api_key)],
    )



def calculate_winner(connection, battle) -> int:
    """
    Calculate the winner of a battle based on the votes and character stats.
    """
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
    
    # Calculate the winner based on the votes and character stats
    character1_score = (character2.health / (character1.strength * character1.speed)) * (pow(0.9, battle.vote1))
    character2_score = (character1.health / (character2.strength * character2.speed)) * (pow(0.9, battle.vote2))
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
    else:
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

@router.get("/get/battle/{battle_id}", response_model=BattleResult)
def get_battle_result(battle_id: int):
    """
    Get the result of a battle by its ID.
    """
    with db.engine.begin() as connection:
        battle = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle
                WHERE id = :id
                """
            ),
            [{"id": battle_id}]
        ).one()
        
        
        if battle.end_date > datetime.now():
            return BattleResult(
                battle_id=battle.id,
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
            winner = calculate_winner(connection, battle)
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
            return BattleResult(
                battle_id=battle.id,
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
            char1_id=battle.char1_id,
            char2_id=battle.char2_id,
            vote1=battle.vote1,
            vote2=battle.vote2,
            winner_id=battle.winner_id,
            start=battle.start_date,
            end=battle.end_date,
            finished=True
        )

@router.get("/get/character/{character_id}", response_model=list[BattleResult])
def character_participation(character_id: int):
    """
    Get a list of battles a character has fought in.
    """
    battles = []
    print("[DEBUG] Getting battles for character")
    with db.engine.begin() as connection:
        # Get all battles for the character
        battlelist = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle
                WHERE char1_id = :char OR char2_id = :char
                """
            ),
            [{"char": character_id}]
        ).fetchall()
        
        # If no battles are found, return an empty list
        if not battlelist:
            print("[DEBUG] No battles found for character")
            return []
        
        for r in battlelist:
            if r.end_date > datetime.now():
                print("[DEBUG] Battle is still active")
                finished = False
            else:
                finished = True
                print("[DEBUG] Battle has ended")
            # Check if the winner is set
            if r.winner_id is None and finished:
                print("[DEBUG] Winner is not set, calculating winner")
                winner = calculate_winner(connection, r)
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE battle
                        SET winner_id = :winner
                        WHERE id = :id
                        """
                    ),
                    [{"winner": winner, "id": r.id}]
                )
                print(f"[DEBUG] Winner of {r.id} calculated and appending battle result")
                battles.append(
                    BattleResult(
                        battle_id=r.id,
                        char1_id=r.char1_id,
                        char2_id=r.char2_id,
                        vote1=r.vote1,
                        vote2=r.vote2,
                        winner_id=winner,
                        start=r.start_date,
                        end=r.end_date,
                        finished=finished
                    )
                )  
            elif r.winner_id is None and not finished:
               # If the battle is still active and the winner is not set, just append the battle result
                print(f"[DEBUG] Battle {r.id} is still active and winner is not set, appending battle result")
                battles.append(
                    BattleResult(
                        battle_id=r.id,
                        char1_id=r.char1_id,
                        char2_id=r.char2_id,
                        vote1=r.vote1,
                        vote2=r.vote2,
                        winner_id=None,
                        start=r.start_date,
                        end=r.end_date,
                        finished=finished
                    )
                )
            else:
                # If the winner is already set, just append the battle result
                print(f"[DEBUG] Winner of battle {r.id} is already set, appending battle result")
                battles.append(
                    BattleResult(
                        battle_id=r.id,
                        char1_id=r.char1_id,
                        char2_id=r.char2_id,
                        vote1=r.vote1,
                        vote2=r.vote2,
                        winner_id=r.winner_id,
                        start=r.start_date,
                        end=r.end_date,
                        finished=finished
                    )
                )
    print(f"[DEBUG] Returning {len(battles)} battles for character {character_id}")
    return battles
            

@router.get("/get/user/{user_id}", response_model=list[BattleResult])
def user_participation(user_id: int):
    """
    Get a list of battles a user has participated in.
    """
    battles = []
    print("[DEBUG] Getting battles for user")
    with db.engine.begin() as connection:
        battlelist = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM battle
                WHERE user_id = :user
                """
            ),
            [{"user": user_id}]
        ).fetchall()
        # If no battles found, return an empty list
        if not battlelist:
            print("[DEBUG] No battles found for user")
            return []
        
        for r in battlelist:
            # Check if the battle has ended
            if r.end_date > datetime.now():
                finished = False
            else:
                finished = True
            # Check if the winner is set
            if r.winner_id is None:
                # Calculate the winner if not already set
                winner = calculate_winner(connection, r)
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE battle
                        SET winner_id = :winner
                        WHERE id = :id
                        """
                    ),
                    [{"winner": winner, "id": r.id}]
                )
                # Append the battle result
                battles.append(
                    BattleResult(
                        battle_id=r.id,
                        char1_id=r.char1_id,
                        char2_id=r.char2_id,
                        vote1=r.vote1,
                        vote2=r.vote2,
                        winner_id=winner,
                        start=r.start_date,
                        end=r.end_date,
                        finished=finished
                    )
                )
            else:
                # If the winner is already set, just append the battle result
                battles.append(
                    BattleResult(
                        battle_id=r.id,
                        char1_id=r.char1_id,
                        char2_id=r.char2_id,
                        vote1=r.vote1,
                        vote2=r.vote2,
                        winner_id=r.winner_id,
                        start=r.start_date,
                        end=r.end_date,
                        finished=finished
                    )
                )
    return battles

@router.post("/vote/{user_id}/{battle_id}/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def battle_vote(user_id: int, battle_id: int, character_id: int):
    """
    Vote for a character during an active battle.
    """    
    with db.engine.begin() as connection:
        
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
            raise HTTPException(status_code=404, detail="Battle not found")
        
        # Check if the battle is still active
        if battle.end_date < datetime.now():
            raise HTTPException(status_code=400, detail="Battle has ended")
        
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
                raise HTTPException(status_code=400, detail="User has already voted")
            
            # Insert the vote into the database
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO battle_votes (battle_id, user_id)
                    VALUES (:battle, :user)
                    """
                ),
                [{"battle": battle_id,
                  "user": user_id}]
            )
            # Update the vote count in the battle table
            if character_ids.char1_id == character_id:
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE battle
                        SET vote1 = vote1 + 1
                        WHERE id = :id
                        """
                    ),
                    [{"id": battle_id}]
                )
            else:
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE battle
                        SET vote2 = vote2 + 1
                        WHERE id = :id
                        """
                    ),
                    [{"id": battle_id}]
                )
        else:
            raise HTTPException(status_code=400, detail="Character not in battle")

@router.post("/make", response_model=BattleCreateResponse)
def create_battle(Battle: Battle):
    """
    Create a battle between two characters and return its id.
    """
    # Assuming duration is in hours
    
    print("[DEBUG] Creating battle")
    
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=Battle.duration)
    
    with db.engine.begin() as connection:
        print("[DEBUG] Inserting battle into database")
        battle_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO battle (user_id, char1_id, char2_id, vote1, vote2, start_date, end_date)
                VALUES (:user, :char1, :char2, :vote1, :vote2, :start, :end)
                RETURNING id
                """
            ),
            [{"user": Battle.user_id,
              "char1": Battle.char1_id,
              "char2": Battle.char2_id,
              "vote1": 0,
              "vote2": 0,
              "start": start_time,
              "end": end_time
              }]
        ).scalar_one()
        
    return BattleCreateResponse(
        battle_id=battle_id,
        char1_id=Battle.char1_id,
        char2_id=Battle.char2_id,
        duration=Battle.duration,
        start=start_time,
        end=end_time
    )
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Character(BaseModel):
    name: str
    description: str
    strength: float
    speed: float
    health: float
    
class ReturnedCharacter(BaseModel):
    char_id: int
    user_id: int
    name: str
    description: str
    rating: float
    strength: float
    speed: float
    health: float 
    
class CharacterMakeResponse(BaseModel):
    char_id: int
    user_id: int
    name: str
    description: str
    rating: float
    strength: float
    speed: float
    health: float 
    
class Franchise(BaseModel):
    name: str
    description: str
    
class FranchiseReturnResponse(BaseModel):
    id: int
    name: str
    description: str
    
class FranchiseMakeResponse(BaseModel):
    id: int
    name: str
    description: str

class FranchiseCharacterAssignment(BaseModel):
    franchise_id: int
    
class C_Review(BaseModel):
    user_id: int
    char_id: int
    comment: str
    
class F_Review(BaseModel):
    user_id: int
    fran_id: int
    comment: str
    
class Battle(BaseModel):
    user_id: int    
    char1_id: int
    char2_id: int
    duration: int # Hours is how its currently implemented across battle.py

class BattleCreateResponse(BaseModel):
    battle_id: int
    char1_id: int
    char2_id: int
    duration: int
    start: datetime
    end: datetime
    
class BattleResult(BaseModel):
    battle_id: int
    user_id: int
    char1_id: int
    char2_id: int
    winner_id: Optional[int]
    start: datetime
    end: datetime
    finished: bool
    
class BattleVoteResponse(BaseModel):
    message: str
    battle_id: int
    char_id: int

class User(BaseModel):
    id: int
    name: str
    
class UserCreate(BaseModel):
    name: str

class User_Favorites(BaseModel):
    favorite_character_id: Optional[int]
    favorite_franchise_id: Optional[int]
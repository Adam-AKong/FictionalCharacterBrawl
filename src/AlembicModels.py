from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.sql.functions import now

Base = declarative_base()

# This is the User Table that stores the users
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True) # Unique ID
    name = Column(String(30), unique=True, nullable=False) # Unique Name
    fav_char_id = Column(Integer, ForeignKey('character.id'), nullable=True) # Optional foreign character ID
    fav_fran_id = Column(Integer, ForeignKey('franchise.id'), nullable=True) # Optional foreign franchise ID
    createed_at = Column(DateTime, server_default=func.now()) # When the user was created

# This is the Character Reviews Table that stores all the reviews for Characters
class C_Review(Base):
    __tablename__ = "c_review"
    
    id = Column(Integer, primary_key=True) # Unique Review ID
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False) # User ID
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False) # Char ID
    comment = Column(String(500), nullable=False) # Comment
    created_at = Column(DateTime, server_default=func.now()) # Created At
    
    # This is a unique constraint to ensure that a user can only review a character once
    __table_args__ = (
        UniqueConstraint('user_id', 'char_id', name='uq_user_char_review'),
    )
    
# This is the Franchise Reviews Table that stores all the reviews for Franchises
class F_Review(Base):
    __tablename__ = "f_review"
    
    id = Column(Integer, primary_key=True) # Unique Franchise ID
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False) # User ID
    franchise_id = Column(Integer, ForeignKey('franchise.id'), nullable=False) # Franchise ID
    comment = Column(String(500), nullable=False) # Comment
    created_at = Column(DateTime, server_default=func.now()) # Created At
     
    # This is a unique constraint to ensure that a user can only review a franchise once
    __table_args__ = (
        UniqueConstraint('user_id', 'franchise_id', name='uq_user_fran_review'),
    )
    
# This is the Character Table that stores all the data on Characters created 
class Character(Base):
    __tablename__ = "character"
    
    id = Column(Integer, primary_key=True) # Unique ID
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False) # User who created
    name = Column(String(30), nullable=False) # Name of Character
    description = Column(String(150), nullable=False) # Description of Character
    rating = Column(Float, nullable=False) # The rating of the Character
    strength = Column(Float, nullable=False) # Strength of the Character
    speed = Column(Float, nullable=False) # Speed of the Character
    health = Column(Float, nullable=False) # Health of the Character
    created_at = Column(DateTime, server_default=func.now()) # Created At
    
# Many to Many table to store Characters assigned to Franchises
class CharFran(Base):
    __tablename__ = "char_fran"
    
    id = Column(Integer, primary_key=True) # Unique ID 
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False) # Character ID
    franchise_id = Column (Integer, ForeignKey('franchise.id'), nullable=False) # Franchise ID
    
# This is the Franchise Table that stores all the data on Franchises created
class Franchise(Base):
    __tablename__ = "franchise"
    
    id = Column(Integer, primary_key=True) # Unique ID
    name = Column(String(50), unique=True, nullable=False) # Unique Name
    description = Column(String(200), nullable=False) # Description of the Franchise
    created_at = Column(DateTime, server_default=func.now()) # Created At
    
# This is the Battle Table that stores all the data on Battles Created 
class Battle(Base):
    __tablename__ = "battle"

    id = Column(Integer, primary_key=True) # Unique ID
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) # User ID who Createed
    char1_id = Column(Integer, ForeignKey('character.id'), nullable=False) # Char1 ID
    char2_id = Column(Integer, ForeignKey('character.id'), nullable=False) # Char2 ID
    winner_id = Column(Integer, ForeignKey('character.id'), nullable=True) # The Winner of the battle
    start_date = Column(DateTime, default=now(), nullable=False) # Start Date 
    end_date = Column(DateTime, nullable=False) # End Date determined by duration
    
# This is the BattleVotes Table that stores all the data the Users Votes
class BattleVotes(Base):
    __tablename__ = "battle_votes"

    id = Column(Integer, autoincrement=True, primary_key=True) # Unique ID
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False) # Character the User is Voting for
    battle_id = Column(Integer, ForeignKey('battle.id'), nullable=False) # The Battle the User is specifying
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) # The User who is voting
    created_at = Column(DateTime, server_default=func.now()) # Created At

    __table_args__ = (
        UniqueConstraint('user_id', 'battle_id', name='uix_user_battle_vote'),
    )

from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.sql.functions import now

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    createed_at = Column(DateTime, server_default=func.now())

    
class C_Review(Base):
    __tablename__ = "c_review"
    
    id = Column(Integer, primary_key=True)
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False)
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    comment = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # This is a unique constraint to ensure that a user can only review a character once
    __table_args__ = (
        UniqueConstraint('user_id', 'char_id', name='uq_user_char_review'),
    )
    
    
class F_Review(Base):
    __tablename__ = "f_review"
    
    id = Column(Integer, primary_key=True)
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False)
    franchise_id = Column(Integer, ForeignKey('franchise.id'), nullable=False)
    comment = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # This is a unique constraint to ensure that a user can only review a franchise once
    __table_args__ = (
        UniqueConstraint('user_id', 'franchise_id', name='uq_user_fran_review'),
    )
    
    
class Character(Base):
    __tablename__ = "character"
    
    id = Column(Integer, primary_key=True)
    user_id = Column (Integer, ForeignKey('user.id'), nullable=False) 
    name = Column(String(30), nullable=False)
    description = Column(String(150), nullable=False)
    rating = Column(Float, nullable=False)
    strength = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    health = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    
class CharFran(Base):
    __tablename__ = "char_fran"
    
    id = Column(Integer, primary_key=True)
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False) 
    franchise_id = Column (Integer, ForeignKey('franchise.id'), nullable=False) 
    
    
class Franchise(Base):
    __tablename__ = "franchise"
    
    id = Column(Integer, primary_key=True) 
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    
class Battle(Base):
    __tablename__ = "battle"

    id = Column(Integer, primary_key=True)      
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)     
    char1_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    char2_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('character.id'), nullable=True)
    start_date = Column(DateTime, default=now(), nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    
class BattleVotes(Base):
    __tablename__ = "battle_votes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    char_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    battle_id = Column(Integer, ForeignKey('battle.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

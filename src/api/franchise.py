import re
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from src.api import auth

from src.api.models import Franchise, FranchiseMakeResponse, Returned_Review

router = APIRouter(
    prefix="/franchise", 
    tags=["Franchise"],
    dependencies=[Depends(auth.get_api_key)],)


USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")

@router.get("/by_id/{franchise_id}", response_model=FranchiseMakeResponse)
def get_franchise_by_id(franchise_id: int):
    """
    Get franchise by ID.
    """
    
    with db.engine.begin() as connection:
        franchise = connection.execute(
            sqlalchemy.text("""
                SELECT name, description
                FROM franchise
                WHERE id = :id
            """),
            {
                "id": franchise_id
                }
        ).one()
        
        if franchise is None:
            raise HTTPException(status_code=404, detail="Franchise not found")
        
        return FranchiseMakeResponse(
            id=franchise_id,
            name=franchise.name,
            description=franchise.description
        )
        

@router.get("/by_name/{franchise_name}", response_model=FranchiseMakeResponse)
def get_franchise_by_name(franchise_name: str):
    """
    Get franchise by name.
    """
    
    with db.engine.begin() as connection:
        franchise = connection.execute(
            sqlalchemy.text("""
                SELECT id, name, description
                FROM franchise
                WHERE name = :franchise_name
            """),
            {
                "franchise_name": franchise_name
                }
        ).one()
        
        if franchise is None:
            raise HTTPException(status_code=404, detail="Franchise not found")
        
        return FranchiseMakeResponse(
            id=franchise.id,
            name=franchise_name,
            description=franchise.description
        )

@router.post("/make", response_model=FranchiseMakeResponse)
def make_franchise(franchise: Franchise):
    """
    Create a new franchise.
    """

    if not USERNAME_REGEX.fullmatch(franchise):
        raise HTTPException(
            status_code=400,
            detail="Franchise must only contain letters, numbers, dashes, or underscores"
        )

    # We need to add later that there can only be 1 franchise
    with db.engine.begin() as connection:
        fran_id = connection.execute(
            sqlalchemy.text("""
                INSERT INTO franchise (name, description)
                VALUES (:name, :description)
                RETURNING id
            """),
            {
                "name": franchise.name,
                "description": franchise.description,
            },
        ).scalar_one()

    new_franchise = FranchiseMakeResponse(
        id = fran_id,
        name = franchise.name,
        description = franchise.description
    )
    return new_franchise

        


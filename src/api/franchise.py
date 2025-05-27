from fastapi import APIRouter, HTTPException, status, Depends
import sqlalchemy
from src import database as db
from src.api import auth

from src.api.models import Franchise, FranchiseMakeResponse

router = APIRouter(
    prefix="/franchise", 
    tags=["Franchise"],
    dependencies=[Depends(auth.get_api_key)],)


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
        ).one_or_none()
        
        if franchise is None:
            raise HTTPException(status_code=404, detail=f"Franchise with id={franchise_id} not found")
        
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
        ).one_or_none()
        
        if franchise is None:
            raise HTTPException(status_code=404, detail=f"Franchise with name '{franchise_name}' not found")
        
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
    
    if not franchise.name:
        raise HTTPException(status_code=400, detail="Franchise name cannot be empty")
    if not franchise.description:
        raise HTTPException(status_code=400, detail="Franchise description cannot be empty")
    
    
    with db.engine.begin() as connection:
        # check if franchise name already exists
        existing_franchise = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM franchise
                WHERE name = :name
            """),
            {
                "name": franchise.name,
            },
        ).scalar_one_or_none()
        
        if existing_franchise is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Franchise with name '{franchise.name}' already exists"
            )
        
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

        


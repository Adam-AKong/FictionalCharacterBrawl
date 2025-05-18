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

@router.get("/get/by_id/{franchise_id}", response_model=FranchiseMakeResponse)
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
        

@router.get("/get/by_name/{franchise_name}", response_model=FranchiseMakeResponse)
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

@router.post("/review/{franchise_id}", status_code=status.HTTP_204_NO_CONTENT)
def make_franchise_review(user_id: int, franchise_id: int, comment: str):
    """
    Make a review for a franchise.
    """
    # Placeholder for actual database call
    if not comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    # No issue with duplicate comments here, just franchises.
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                INSERT INTO f_review (user_id, franchise_id, comment)
                VALUES (:user_id, :franchise_id, :comment)
            """),
            {
                "user_id": user_id,
                "franchise_id": franchise_id,
                "comment": comment,
            },
        )
        
@router.get("/get_review/{franchise_id}", response_model=list[Returned_Review])
def get_franchise_review(franchise_id: int):
    """
    Get all reviews for a given franchise referencing its id.
    """
    with db.engine.begin() as connection:
        comments = connection.execute(
            sqlalchemy.text("""
                SELECT user_id, comment
                FROM f_review
                WHERE franchise_id = :fran_id
            """),
            {
                "fran_id": franchise_id
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

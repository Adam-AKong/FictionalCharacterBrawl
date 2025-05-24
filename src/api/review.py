from fastapi import APIRouter, HTTPException, status, Depends
import sqlalchemy
from src import database as db

from src.api.models import Returned_Review
from src.api import auth

router = APIRouter(
    prefix="/review", 
    tags=["Review"],
    dependencies=[Depends(auth.get_api_key)],)

@router.post("/character/create/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def review_character(user_id: int, character_id: int, comment: str):
    """
    Review a character.
    """
    if not comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                INSERT INTO c_review (user_id, char_id, comment)
                VALUES (:user_id, :char_id, :comment)
            """),
            {
                "user_id": user_id,
                "char_id": character_id,
                "comment": comment
            },
        )
        
@router.get("/character/list/{character_id}", response_model=list[Returned_Review])
def get_character_review(character_id: int):
    """
    Get all reviews for a given character referencing its id.
    """
    with db.engine.begin() as connection:
        comments = connection.execute(
            sqlalchemy.text("""
                SELECT user_id, comment
                FROM c_review
                WHERE char_id = :char_id
            """),
            {
                "char_id": character_id
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



@router.post("/franchise/create/{franchise_id}", status_code=status.HTTP_204_NO_CONTENT)
def make_franchise_review(user_id: int, franchise_id: int, comment: str):
    """
    Make a review for a franchise.
    """
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



@router.get("/franchise/list/{franchise_id}", response_model=list[Returned_Review])
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
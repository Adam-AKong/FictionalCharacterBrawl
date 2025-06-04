from fastapi import APIRouter, HTTPException, Depends
import sqlalchemy
from src import database as db
from src.api.character import get_character_by_id
from src.api.franchise import get_franchise_by_id
from src.api.models import C_Review, F_Review
from src.api import auth
from src.api.user import get_user

import time

router = APIRouter(
    prefix="/review", 
    tags=["Review"],
    dependencies=[Depends(auth.get_api_key)],)

@router.post("/character/create/", response_model=C_Review)
def review_character(review: C_Review):
    """
    Review a character.
    """
    if not review.comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    with db.engine.begin() as connection:
        # If conflict occurs, it means the user has already reviewed this character.
        # Update the existing review instead of inserting a new one.
        
        # Check if user id and char id are valid
        # This will return a  HTTP exception from the function it is calling itself
        get_user(review.user_id)
        get_character_by_id(review.char_id)

        
        connection.execute(
            sqlalchemy.text("""
                INSERT INTO c_review (user_id, char_id, comment)
                VALUES (:user_id, :char_id, :comment)
                ON CONFLICT (user_id, char_id) DO UPDATE
                SET comment = EXCLUDED.comment
            """),
            {
                "user_id": review.user_id,
                "char_id": review.char_id,
                "comment": review.comment,
            },
        )
    return C_Review(
        user_id = review.user_id,
        char_id = review.char_id,
        comment = review.comment
    )
    
@router.get("/character/list/{character_id}/{page_number}", response_model=list[C_Review])
def get_character_review(character_id: int, page_number: int):
    """
    Get all reviews for a given character referencing its id.
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
        
        # Get all comments for the character
        page_size = 10
        offset = page_number * page_size

        query = sqlalchemy.text(f"""
            SELECT user_id, comment
            FROM c_review
            WHERE char_id = :char_id
            LIMIT {page_size} OFFSET {offset}
        """)

        comments = connection.execute(query, {
            "char_id": character_id
        }).all()

                # If no comments found, return an empty list
        if not comments:
            return []

        all_comments = []
        for comment in comments:
            # Create a list of C_Review objects from the comments
            all_comments.append(
                C_Review(
                    user_id = comment.user_id,
                    char_id = character_id,
                    comment = comment.comment
                )
            )

        return all_comments

@router.post("/franchise/create", response_model=F_Review)
def make_franchise_review(review: F_Review):
    """
    Make a review for a franchise.
    """
    if not review.comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    
    # Check if user id and fran id are valid
    # This will return a  HTTP exception from the function it is calling itself
    get_user(review.user_id)
    get_franchise_by_id(review.fran_id)

    # If conflict occurs, it means the user has already reviewed this character.
    # Update the existing review instead of inserting a new one.
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                INSERT INTO f_review (user_id, franchise_id, comment)
                VALUES (:user_id, :franchise_id, :comment)
                ON CONFLICT (user_id, franchise_id) DO UPDATE
                SET comment = EXCLUDED.comment
            """),
            {
                "user_id": review.user_id,
                "franchise_id": review.fran_id,
                "comment": review.comment,
            },
        )
    
    return F_Review(
        user_id = review.user_id,
        fran_id = review.fran_id,
        comment = review.comment
    )

@router.get("/franchise/list/{franchise_id}/{page_number}", response_model=list[F_Review])
def get_franchise_review(franchise_id: int, page_number: int):
    """
    Get all reviews for a given franchise referencing its id.
    """
    
    if page_number < 0:
        raise HTTPException(status_code=400, detail=f"Page Number must not be negative")
    
    with db.engine.begin() as connection:
        # Check if franchise exists
        franchise_exists = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM franchise
                WHERE id = :fran_id
            """),
            {
                "fran_id": franchise_id
            }
        ).one_or_none()
        
        if franchise_exists is None:
            raise HTTPException(status_code=404, detail=f"Franchise with id={franchise_id} not found")
        
        # Get all comments for the franchise
        page_size = 10
        offset = page_number * page_size
        
        query = sqlalchemy.text(f"""
            SELECT user_id, comment
            FROM f_review
            WHERE franchise_id = :fran_id
            LIMIT {page_size} OFFSET {offset}
        """)
        
        comments = connection.execute(query, {
            "fran_id": franchise_id
        }).all()
        
        # If no comments found, return an empty list
        if not comments:
            return []

        all_comments = []
        # Create a list of F_Review objects from the comments
        for comment in comments:
            all_comments.append(
                F_Review(
                    user_id = comment.user_id,
                    fran_id = franchise_id,
                    comment = comment.comment
                )
            )

        return all_comments
    
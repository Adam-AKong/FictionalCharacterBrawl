from fastapi import APIRouter, HTTPException, Depends
import sqlalchemy
from src import database as db
from src.api.models import C_Review, F_Review
from src.api import auth

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
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO c_review (user_id, char_id, comment)
                VALUES (:user_id, :char_id, :comment)
                ON CONFLICT (user_id, char_id) DO UPDATE
                SET comment = EXCLUDED.comment
                """
                ),
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
    
        
@router.get("/character/list/{character_id}", response_model=list[C_Review])
def get_character_review(character_id: int):
    """
    Get all reviews for a given character referencing its id.
    """
    with db.engine.begin() as connection:
        # Check if character exists
        character_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM character
                WHERE id = :char_id
                """
                ),
            {
                "char_id": character_id
            }
        ).one_or_none()
        
        if character_exists is None:
            raise HTTPException(status_code=404, detail=f"Character with id={character_id} not found")
        
        # Get all comments for the character
        comments = connection.execute(
            sqlalchemy.text(
                """
                SELECT user_id, comment
                FROM c_review
                WHERE char_id = :char_id
                """
                ),
            {
                "char_id": character_id
            }
        ).all()
        
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

    # If conflict occurs, it means the user has already reviewed this character.
    # Update the existing review instead of inserting a new one.
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO f_review (user_id, franchise_id, comment)
                VALUES (:user_id, :franchise_id, :comment)
                ON CONFLICT (user_id, franchise_id) DO UPDATE
                SET comment = EXCLUDED.comment
                """
                ),
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



@router.get("/franchise/list/{franchise_id}", response_model=list[F_Review])
def get_franchise_review(franchise_id: int):
    """
    Get all reviews for a given franchise referencing its id.
    """
    with db.engine.begin() as connection:
        # Check if franchise exists
        franchise_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM franchise
                WHERE id = :fran_id
                """
                ),
            {
                "fran_id": franchise_id
            }
        ).one_or_none()
        
        if franchise_exists is None:
            raise HTTPException(status_code=404, detail=f"Franchise with id={franchise_id} not found")
        
        # Get all comments for the franchise
        comments = connection.execute(
            sqlalchemy.text(
                """
                SELECT user_id, comment
                FROM f_review
                WHERE franchise_id = :fran_id
                """
                ),
            {
                "fran_id": franchise_id
            }
        ).all()
        
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
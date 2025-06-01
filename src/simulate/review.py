from faker import Faker
import random
from src.api.review import review_character, make_franchise_review
from src.api.models import C_Review, F_Review
import time

fake = Faker()

# Simulates both Character and Franchise Reviews
def simulate_reviews(total: int, max_user_id: int, max_char_id: int, max_fran_id: int):
    start = time.time()
    for i in range(total):
        try:
            # Even iterations → Character Review
            review = C_Review(
                user_id=random.randint(1, max_user_id),
                char_id=random.randint(1, max_char_id),
                comment=fake.sentence(nb_words=10)
            )
            review_character(review)
            # Odd iterations → Franchise Review
            review = F_Review(
                user_id=random.randint(1, max_user_id),
                fran_id=random.randint(1, max_fran_id),
                comment=fake.sentence(nb_words=10)
            )
            make_franchise_review(review)

            if i % 1000 == 0 and i != 0:
                elapsed = time.time() - start
                print(f"{i:,} reviews created in {elapsed:.2f} seconds")

        except Exception as e:
            print(f"Error on review {i}: {e}")
            continue

    print(f"Done — {total:,} reviews created in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    review_total = 1_000
    user_total = 1_000
    character_total = 1_000
    franchise_total = 1_000
    simulate_reviews(review_total, user_total, character_total, franchise_total)

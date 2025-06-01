from faker import Faker
import random
from src.api.character import make_character
from src.api.models import Character, FranchiseCharacterAssignment
import time

fake = Faker()

def simulate_characters(total: int):
    max_user_id = total
    max_franchise_id = total
    start = time.time()
    for i in range(total):
        try:
            # Create fake character data
            character_data = Character(
                name = f"{fake.first_name()} {i}",
                description=fake.text(max_nb_chars=150),
                strength=random.uniform(1, 999),
                speed=random.uniform(1, 999),
                health=random.uniform(1, 999)
            )

            # Random user ID from previously inserted users
            user_id = random.randint(1, max_user_id)

            # Random franchise assignment(s)
            assigned_franchises = [
                FranchiseCharacterAssignment(franchise_id=random.randint(1, max_franchise_id))
                for _ in range(random.randint(1, 5))  # 1–5 franchises per character
            ]

            # Call the actual creation logic
            make_character(user_id=user_id, character=character_data, franchiselist=assigned_franchises)

            if i % 1000 == 0 and i != 0:
                elapsed = time.time() - start
                print(f"{i:,} characters created in {elapsed:.2f} seconds")

        except Exception as e:
            print(f"Error on character {i}: {e}")
            continue

    print(f"Done — {total:,} characters created in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    simulate_characters()

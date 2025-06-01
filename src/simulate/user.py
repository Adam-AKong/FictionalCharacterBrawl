import sys, os

from src.api.models import UserCreate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from faker import Faker
import time
import re

from src.api.user import make_user
fake = Faker()

def clean_username(raw_name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", raw_name)

def generate_username(fake, i):
    base = fake.user_name()
    return f"{base}_{i}"

def simulate_users(total: int):
    start = time.time()
    for i in range(total):
        try:
            username = UserCreate(
                name = clean_username(generate_username(fake, i))
            )
            make_user(username)

            # Progress logging every 10,000 inserts
            if i % 1_000 == 0 and i != 0:
                elapsed = time.time() - start
                print(f"{i:,} users created in {elapsed:.2f} seconds")

        except Exception as e:
            print(f"Error on user {i}: {e}")
            continue

    print(f"Done — {total:,} users created in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    user_total = 1_000
    simulate_users(user_total)
    

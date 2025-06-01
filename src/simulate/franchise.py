from faker import Faker
from src.api.franchise import make_franchise  # your actual logic
from src.api.models import Franchise            # your Pydantic model
import time

fake = Faker()

def simulate_franchises(total: int):
    start = time.time()
    for i in range(total):
        try:
            franchise = Franchise(
                name=f"{fake.unique.company()} {i}",  # add index to avoid dupes
                description=fake.text(max_nb_chars=200)
            )
            make_franchise(franchise)

            if i % 1000 == 0 and i != 0:
                elapsed = time.time() - start
                print(f"{i:,} franchises created in {elapsed:.2f} seconds")

        except Exception as e:
            print(f"Error on franchise {i}: {e}")
            continue

    print(f"Done — {total:,} franchises created in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    franchise_total = 1_000
    simulate_franchises(franchise_total)

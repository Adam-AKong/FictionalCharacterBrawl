from faker import Faker
import random
import time
from src.api.battle import create_battle, battle_vote
from src.api.models import Battle

fake = Faker()

def simulate_battles(total: int, max_user_id: int, max_char_id: int):
    start = time.time()
    for i in range(total):
        try:
            char1_id = random.randint(1, max_char_id)
            char2_id = char1_id
            while char2_id == char1_id:
                char2_id = random.randint(1, max_char_id)

            duration = random.randint(0, 6)

            battle_data = Battle(
                user_id=random.randint(1, max_user_id),
                char1_id=char1_id,
                char2_id=char2_id,
                duration=duration
            )

            battle_response = create_battle(battle_data)
            battle_id = battle_response.battle_id  # assuming your response includes this

            # Simulate votes only if duration > 0
            if duration > 0:
                num_votes = random.randint(1, 10)  # simulate 1–10 votes per battle
                for _ in range(num_votes):
                    voter_id = random.randint(1, max_user_id)
                    voted_char_id = random.choice([char1_id, char2_id])
                    try:
                        battle_vote(user_id=voter_id, battle_id=battle_id, character_id=voted_char_id)
                    except Exception as ve:
                        # Possibly duplicate vote; ignore for simulation
                        continue

            if i % 1000 == 0 and i != 0:
                elapsed = time.time() - start
                print(f"{i:,} battles created in {elapsed:.2f} seconds")

        except Exception as e:
            print(f"Error on battle {i}: {e}")
            continue

    print(f"Done — {total:,} battles created in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    battle_total = 1_000
    user_total = 1_000
    character_total = 1_000
    simulate_battles(battle_total, user_total, character_total)

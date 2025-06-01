from src.simulate import battle, character, franchise, review, user

if __name__ == "__main__":
    # This will simulate running the create endpoints of each of these sections
    print("Starting the Simulation")
    total = 1_000_000
    # 1 million users
    user.simulate_users(total)
    # 1 million franchises
    franchise.simulate_franchises(total)
    # 1 million characters
    character.simulate_characters(total)
    # 1 million reviews of both franchise and character
    review.simulate_reviews(total)
    # 1 million battles along with voting
    battle.simulate_battles(total)
    print("Simulation Complete")
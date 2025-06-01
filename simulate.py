from src.simulate import battle, character, franchise, review, user

if __name__ == "__main__":
    # This will simulate running the create endpoints of each of these sections
    print("Starting the Simulation")
    user_total = 100_000
    franchise_total = 50_000
    character_total = 150_000 # There will be more inserts due to the many to many relationship with char/fran, 1-5 franchises per character
    review_total = 200_000 # Double this since it does franchise and character at the same time
    battle_total = 300_000 # There will be more inserts due to there being 0-10 votes per battle

    user.simulate_users(user_total)
    franchise.simulate_franchises(franchise_total)
    character.simulate_characters(character_total, user_total, franchise_total)
    review.simulate_reviews(review_total, user_total, character_total, franchise_total)
    battle.simulate_battles(battle_total, user_total, character_total)
    print("Simulation Complete")
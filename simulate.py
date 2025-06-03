from src.simulate import battle, character, franchise, review, user

if __name__ == "__main__":
    # This will simulate running the create endpoints of each of these sections
    print("Starting the Simulation")
    user_total = 200_000
    franchise_total = 1_000
    character_total = 50_000 # There will be more inserts due to the many to many relationship with char/fran, 1-5 franchises per character
    review_total = 200_000 # Double this since it does franchise and character at the same time
    battle_total = 50_000 # There will be more inserts due to there being 0-10 votes per battle
    
    # Estimated Rows
    # user_total = 200,000
    # franchise_total = 1,000
    # character_total = 150,000 = 50,000 * 3 average franchises per character
    # review_total = 400,000 = 200,000 * 2 (franchise and character reviews)
    # battle_total = 250,000 = 50,000 * 5 (average votes per battle)
    # Total estimated rows ~ 1,000,000

    user.simulate_users(user_total)
    franchise.simulate_franchises(franchise_total)
    character.simulate_characters(character_total, user_total, franchise_total)
    review.simulate_reviews(review_total, user_total, character_total, franchise_total)
    battle.simulate_battles(battle_total, user_total, character_total)
    print("Simulation Complete")
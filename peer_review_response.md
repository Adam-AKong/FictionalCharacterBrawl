## Schema/API
# Spency Perley  
1. Keeping user table as user. While it is a keyword, it is still able to function by surrounding it with quotes.
2. While I understand the concern of abbreviated names such as c_review, and f_review. I believe it isn't difficult at all to determine what they are refering to especially within the scope of what the API endpoints are accomplishing.
3. We are keeping the /get/by_id/{id} since we also have the /get/by_name/{username}. This is to differentiate the 2 endpoints to avoid confusion later on. Although Character endpoints don't have a /get/by_name we are keeping the by_id as it keeps the endpoint naming schema consistent
4. Each battle only contains 2 characters. I'm not sure exactly what we would need to change to resolve this comment. A character can be in multiple battles at once as each battle is independent of each other. From how I understand it, characters and battles are already in a Many to Many relationship in which a specific battle must have 2 characters but a character doesn't need to be in a battle.
5. Battle's being in a schrodingers cat situation was intentional as we don't want to implement a system to automatically update the battles as soon as the battle end duration is over. This is due to a complexity that is uneccessary and is solved by only updating when information is requested. Each endpoint that returns data first checks if the battle is over, if not return correct information, if battle is over, check if the winner has been decided. If winner has been decided, then return correct information, if not, calculate winner and return correct information.
6. An endpoint to determine the battle results is uneccessary due to the reasoning above. Especially since the suggestion is irrespective of battle being finished or not, as if a battle isn't finished, a battle winner should not be calculated. Furthermore, all of the results of this is already tied into the fetching of information on a battle making it redundant. If we were to remove these steps from fetching of information then this endpoint would make sense, but then once again, fetching information on a battle would mean it wouldn't be determining a winner if the battle is over and a winner is not calculated.
7. Moving the getting battle information by character/user to its respective category is an interesting thought. It does make sense since we are requesting all the battle information for that character/user, but it also makes sense to keep it grouped in the battle endpoints category because the requested information is of battles. And honestly not moving it over is less work...
8. Changing endpoints to be more RESTful makes sense. 
9. Making votes many to many makes sense. Votes are now removed from battle table and results are aggregated from battle_votes table
10. Changing made_at to created_at makes sense.
11. Resolved in 9 by aggregating votes from battle_votes table
12. Adding created_at columns for other tables makes sense (battle already has an implicit created_at with start_date)
13. Creating a review route makes sense and this makes it consistent with battle endpoint creating and retrieving information from that route
14. Good thoughts on making inputs URL safe. I believe FastAPI already handles this as I've tried inputting unsafe strings. However, I think this is a justifiable safety measure so limiting the type of characters users can input for strings is important.

# Atkin
1. Reasonable to remove /get to make more RESTful
2. I'm not sure what you mean by /battle/characters/{character_1}/{character_2} since we don't have this endpoint
3. Constraints on character stats is neccessary
4. I think its uneccessary to add the information of character_id instead of id, since its already implied its the id for the character table, etc.
5. Changing battle votes to aggregate is a good idea
6. While I understand the concern of abbreviated names such as c_review, and f_review. I believe it isn't difficult at all to determine what they are refering to especially within the scope of what the API endpoints are accomplishing.
7. This seems more like a code review comment, but yes removing redudant files is important
8. I don't see how the id can overlap as they are different endpoints going to different tables
9. vote1 and vote2 are now removed so this doesn't matter anymore
10. Good thoughts, they are no longer nullable
11. I believe you are refering to a json object being returned, which is a good idea to include instead of a no status response
12. Default values I don't think are a good idea since the user is supposed to specify them to make it theirs. However, having constraints on them is a good idea. They now have to be a positive integer.

# Julianne Legados
1. Good thoughts, comments are no longer allowed to be empty
2. I think you are referring to the variable being named char_id while the endpoint puts {character_id}. Good catch
3. I'm not sure what you mean by consistent id naming
4. Good catch, some columns that shouldn't be nullable were set to True.
5. This is intended as if a user is deleted, their commens and characters should still remain as they are valid characters/reviews.
6. Characters are allowed to have the same name as there are multiple versions of the same character within franchises. Furthermore, one user might have a different idea of the stats or description for that Character. However, Usernames for Users should be unique which we are now enforcing.
7. We didn't upload our Entity Relationship Diagram, but we do have our AlembicModels.py which we use to auto generate the schema to match the tables created in that file. This serves as the documentation for the tables and relationships.
8. We haven't really decided upon a character balance for stats, plus this isn't really a schema/api concern. I think it's fine for users to create whatever characters they want. Yes the leaderboards can be unfair, but I believe the main focus is upon the actual character creation and review system. Battles are an additional aspect that if users want to create fair and balanced characters or if they want to make a cheat character they can.
9. Duplicated Reviews now just update the previous comment instead of inserting in a new Review
10. This is more of adding an additional endpoint which is a good idea. We might implement the feature to favorite characters/franchises
11. I am confused as to what you mean by unable to view the comments as a list. We have an endpoint that does exactly this which gets all the reviews for a specific character id or franchise id.
12. This is more of adding an additional endpoint which is a good idea. We might implement this feature to delete reviews.

# Ivan Alvarez
1. I'm not sure what you mean by upgrade properly. Alembic upgrade head should cover this properly
2. Franchise Name is now unique overall. However, Character Name is not unique and that is intended as a user might want to create the same character multiple times with different stats or different descriptions.
3. Interesting idea to add a soft deletion of rows, but we might not implement this as this adds a lot of new endpoints to create.
4. Good idea for the filtering option for Listing endpoints, which we might implement.
5. Endpoints now all return proper HTTP Exceptions or a proper JSON object.
6. Not sure why we would need to add bulk characters or franchises at the same time. This can just be accomplished by running the current endpoints multiple time with different variables.
7. Good idea to add authentication for specific endpoints, we might implement this
8. I believe we already have this through our various endpoints in the battle route which calls information from the battle and battle_votes table unless I am misunderstanding your suggestion
9. Interesting idea to add more detailed information of franchise, character, etc. We might implement this
10. Good idea, adding more timestamps to different tables
11. Start_Date has the default value of now() and end_date is determined based on the duration. However there were no checks to make sure these values were valid so good catch!
12. Stats are the same regardless of Franchise or Character itself. The current formula is 
score2 = (char1_health / (char2_strength * char2_speed)) * (vote_modifier ^ char2_votes)
score1 = (char2_health / (char1_strength * char1_speed)) * (vote_modifier ^ char1_votes)
This works by multipling the characters strength and speed together and dividing it into the opposing characters health. This score is then multiplied by the vote_modifier which is currently set as 0.9 and taking it to the power of the votes for the character. This causes the score to be reduced by 90% exponentially each vote. The lowest score value wins. On a tie, the winner is randomly decided.
However, it could be an interesting idea to implement a franchise power stat which affects characters in that franchise proportionally compared to other franchises. Not sure if we will implement this though.

## Code Review
# Spencer perley
1. Constraints are added to make it so if duplicate Names are sent, it will send an error as Username is unique now
2. Changing some of the .one_or_none() to .scalar_one is just not needed. They are two separate data return calls and should not be treated the same. We specifically want to return one row or none so we can raise an exception. We don't want to return only one column when we need the entire row.
3. Uneccessary Comments are now removed
4. Names now have constraints applied
5. Descriptive responses are now sent
6. Tried making the cursor accessor functions more consistent
7. Checks are added to make it so if duplicate Franchise Names are sent, it will send an error as Franchise is now unique
8. Constraints to what is allowed to be put in the franchise name itself are added.
9. Loggers can be a good idea. Though most of our DEBUG statements were just throwaway to do quick simple debugging while testing. We just forgot to remove them.
10. Understandable that r was not a good variable name. It was meant to be r for result, but with your reasoning I am changing it to b for battle.
11. I personally don't see a problem with this since the context even within the code and database itself is fairly obviously its an abbreviation of character. However, for the specific variable name of "char" I will rename to "character". I won't be changing char1_id, char2_id, etc.
12. The magic number is now removed and is a named constant
13. There are now constraints for character stats to be non negative


# Atkin
1. Most of the codebase doesn't need unit tests as it involves the database. However, adding unit tests for calculating the battle result we could add.
2. Added more info in Readme
3. Debug statements removed
4. Most development comments are removed
5. Not sure what constitutes redundant method comments. Most of method comments are just documentation so I'm not sure what is redundant about them and no examples were given.
6. using fetchall to unindent seems like a cool feature, but its just easier to keep everything within the scope of the database connection call.
7. Not entirely sure what you mean by multiple create statements. I believe you are referring to the Response Models to send as json objects through pydantic models. The reason why there are separate ones is because some endpoints don't need to return the same responses.
8. There already was a helper method to calculate the winner, however, it has also been changed and refined to be more efficient.
9. Added a tiebreaker for a tie. It just picks a random winner now.
10. Not sure what you meant by depending on the if statement, however, the overall system has been tweaked since votes are now aggregated from battle_votes instead of stored in the battle itself
11. Not sure what checks for arguments we need to have as no examples were given.
12. uv run main.py now works
13. Not entirely sure what you mean by "not returning a User class". The endpoints are returning the pydantic model of User which provides the id and the username of that specific User.

# Julianne Legados
1. Good catch, removing the redudant /user when it is already /user is a good idea to make the routes cleaner
2. The votes are now aggregated to avoid multiple sources of truth and to prevent two people clicking fast and voting multiple times
3. Good catch on the concurrency problem for battles. We will make sure to fix that in order to prevent race conditions
4. Changing Battle: Battle into battle_data: Battle is a good idea. It definitely can be confusing when using the same symbol names
5. A helper function is now used to cleanup repetative lines of codes for the 3 endpoints of getting information on battles
6. Unit tests for the most part are uneccessary since it is all database calls. However, I have now changed the helper function of calculating the winner to avoid database calls and unit tests can be run for that.
7. It's a good idea to add a __repr__ for printing, however, its not a necessary change to make since the print functions will be getting removed in the end anyways.
8. Checks for if a character/franchise/user/battle are now in place
9. The variable mismatch is now resolved and it will properly use {character_id} which is consistent with all the other endpoints
10. Constraints are added to make sure the values are not negative or 0. Users are allowed to make their character as strong as they want though.
11. Duplicate names for users are now being checked for.
12. Since users have to input in the value of duration and the duration field is mandatory, I don't believe we need to specify a default value since the user gets to decide (as long as it is greater than 0 and there are now checks for that as well)

# Ivan Alvarez
1. The Readme is now updated
2. If the table is trying to be created when it already exists, that means you already have a table under that port. That means you need to assign the database to a different port.
3. Docstrings to AlembicModels.py is a good idea
4. Removing uneccessary imports is a good idea
5. Removing commented which are unused code is a good idea
6. Removing Programmer notes that are not neccessary anymore is a good idea
7. Removing uneccessary alembic files is a good idea
8. Resolved the issue that was preventing us from doing uv run main.py
9. server.py has been added
10. Unit tests are uneccessary for a majority of the codebase as it is all database calls. However, the newly changed helper function to calculate Battle Winner has been modified to allow for unit tests
11. Proper HTTPExceptions have been added to provide useful information when errors occur
12. API Keys have been added

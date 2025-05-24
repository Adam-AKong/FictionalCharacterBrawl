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
11. 

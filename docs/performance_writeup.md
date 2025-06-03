# Fake Data Modeling
## Code

```uv run simulate.py```

The Code for each section is under src/simulate

## Estimated Total Rows
This is taken from simulate.py

user_total = 200,000
franchise_total = 1,000
character_total = 150,000 = 50,000 * 3 average franchises per character
review_total = 400,000 = 200,000 * 2 (franchise and character reviews)
battle_total = 250,000 = 50,000 * 5 (average votes per battle)
Total estimated rows ~ 1,000,000

I believe the database will scale like this where the majority is focused upon the amount of Users itself. Frachises probably won't get that big as there are only so many popular franchises out there, however I included the possibility of people creating less popular known franchises or even their own custom ones. With 200,000 users, its possible for franchises themself to reach 1,000. Furthermore, I don't expect every user to be creating characters as the vast majority I believe will just use the database to scroll and look at other comments. However, with 150,000 users, some might create multiple while others making none, which is why I estimated 50,000 total characters being made. This is quite a lot even still as that means its an average of 50 characters per franchise. However, duplicate characters can exist as users have the freedom to determine the stats of the characters. Since you can assign multiple franchises, I imagine some users would want to create characters that are involved in multiple franchises due to parady or their own custom franchise/characters made with friends. I estimated that on average a user would want to make 2 reviews each. The simulated data does an even split of characters/franchises, which I don't expect to happen, but for the sake of testing the efficiency of endpoints I decided to implement that. Once again, not every user will create reviews, but the more active ones could potentially create multiple upwards to dozens if not hundreds, while the vast majority will stay silent and just browse the content. Lastly the battles are a secondary source of our project with the main focus being the database of characters franchises. With that being said, I estimated the amount of battles to be less than the reviews as most people probably won't actually care too much about some silly online battle system with unregulated character stats. However, since they are so easy to create and vote upon, I imagine there will be a decent following from active individuals allowing for a solid on average 1 battle for every 4 users. Voting I created to be 0-10 in the simulated data, witt it being 5 on average, making it 250,000 total rows.

# Performance Results of Hitting Endpoints

## Endpoint 1
GET /character/by_id/{character_id}
Description:
Get character by ID.
Runtime: (ms)
0.005954s

## Endpoint 2
GET /character/list/{user_id}
Description:
Get all characters made by user.
Runtime:
0.010645s

## Endpoint 3
GET /character/leaderboard
Description:
Get the leaderboard of characters.
Runtime:
0.019709s

## Endpoint 4
POST /character/make
Description:
Create a new character.
Runtime:
0.007769s

## Endpoint 5
GET /character/franchise/{character_id}
Description:
Get all franchises for a given character referencing its id.
Runtime:
0.014095s

## Endpoint 6
GET /franchise/by_id/{franchise_id}
Description:
Get franchise by ID.
Runtime:
0.005117s

## Endpoint 7
GET /franchise/by_name/{franchise_name}
Description:
Get franchise by name.
Runtime:
0.005311s

## Endpoint 8
POST /franchise/make
Description:
Create a new franchise.
Runtime:
0.006875s

## Endpoint 9
GET /user/by_id/{user_id}
Description:
Get User by ID.
Runtime:
0.005451s

## Endpoint 10
GET /user/by_name/{username}
Description:
Get User by name.
Runtime: 
0.006681s

## Endpoint 11
POST /user/make
Description:
Make a new user.
Runtime: 
0.007802s

## Endpoint 12
POST /user/favorite/character
Description:
Sets a user's favorite character.
Runtime:
0.011942s

## Endpoint 13
GET /user/favorite/character
Description:
Gets a user's favorite character and franchise.
Runtime:
0.005775s

## Endpoint 14
POST /user/favorite/franchise
Description:
Sets a user's favorite franchise.
Runtime:
0.010281s

## Endpoint 15
POST /review/character/create
Description:
Review a character.
Runtime:
0.012631s

## Endpoint 16
GET /review/character/list/{character_id}
Description:
Get all reviews for a given character referencing its id.
Runtime:
0.012530s

## Endpoint 17
POST /review/franchise/create
Description:
Make a review for a franchise.
Runtime:
0.012312s

## Endpoint 18
GET /review/franchise/list/{franchise_id}
Description:
Get all reviews for a given franchise referencing its id.
Runtime:
0.008459s

## Endpoint 19
GET /battle/battle/{battle_id}
Description:
Get the result of a battle by its ID.
Runtime:
0.024302s

## Endpoint 20 (Slowest)
GET /battle/character/{character_id}
Description:
Get a list of battles a character has fought in.
Runtime:
0.042538s

## Endpoint 21
GET /battle/user/{user_id}
Description:
Get a list of battles a user has participated in.
Runtime:
0.036662s

## Endpoint 22
POST /battle/vote/{user_id}/{battle_id}/{character_id}
Description:
Vote for a character during an active battle.
Runtime:
0.008979s

## Endpoint 23
POST /battle/make
Description:
Create a battle between two characters and return its id.
Runtime:
0.008245s

# Performance Tuning

## Initial Test
Our slowest endpoint was GET /battle/character/{character_id}. This was surprising because this endpoint only has one query, and isn’t as technically complex as some of the others. It should just list some battles following a parameter, right?

Upon running:
EXPLAIN SELECT *
FROM battle_with_votes
WHERE char1_id = 1 OR char2_id = 1
LIMIT 10 OFFSET 0

We got:
Limit  (cost=5664.29..5664.53 rows=3 width=52)
  ->  GroupAggregate  (cost=5664.29..5664.53 rows=3 width=52)
        Group Key: b.id
        ->  Sort  (cost=5664.29..5664.33 rows=14 width=40)
              Sort Key: b.id
              ->  Hash Right Join  (cost=1168.20..5664.03 rows=14 width=40)
                    Hash Cond: (bv.battle_id = b.id)
                    ->  Seq Scan on battle_votes bv  (cost=0.00..3874.55 rows=236655 width=8)
                    ->  Hash  (cost=1168.16..1168.16 rows=3 width=36)
                          ->  Seq Scan on battle b  (cost=0.00..1168.16 rows=3 width=36)
                                Filter: ((char1_id = 1) OR (char2_id = 1))

##First Indexing Tweak
The key thing that drives up the cost as the program searches the list is the right join on the ‘battle_vote’ table with the ‘battle’ table. The condition is a comprehensive search for any matches between the two id’s which means that the query ends up scanning all of the battle_vote rows because battle_id isn’t unique or indexed (yet!)

Therefore, in order to improve the efficiency of this join and not have to scan all of the rows for matches, we just need to add an index to battle_id. This will make it easier to reference and join without scanning every row.

So, we created the following index:
CREATE INDEX ON battle_votes(battle_id);

Then, running the same explain query got us this:
Limit  (cost=1194.29..1194.53 rows=3 width=52)
  ->  GroupAggregate  (cost=1194.29..1194.53 rows=3 width=52)
        Group Key: b.id
        ->  Sort  (cost=1194.29..1194.33 rows=14 width=40)
              Sort Key: b.id
              ->  Nested Loop Left Join  (cost=0.42..1194.03 rows=14 width=40)
                    ->  Seq Scan on battle b  (cost=0.00..1168.16 rows=3 width=36)
                          Filter: ((char1_id = 1) OR (char2_id = 1))
                    ->  Index Scan using battle_votes_battle_id_idx on battle_votes bv  (cost=0.42..8.55 rows=7 width=8)
                          Index Cond: (battle_id = b.id)

Pretty much all of the cost of that join has been lost since we added the index. Because iterating through battle_votes was so expensive, this change has cut our overall cost to run into a fifth of what it used to be!

##But It Can Be Better!
To take it one step further, we also realized that the sequential scan for the character ids within battle is expensive, though to a lesser degree. The character ids aren’t unique, so it makes sense that any query would have to search through the entire table to find what it was looking for. Therefore, a way to further optimize the query would be to make two more indexes, on char1_id and char2_id. Here’s the code we used to create them:
CREATE INDEX ON battle(char1_id);
CREATE INDEX ON battle(char2_id);

Re-running explain:
Limit  (cost=46.02..46.26 rows=3 width=52)
  ->  GroupAggregate  (cost=46.02..46.26 rows=3 width=52)
        Group Key: b.id
        ->  Sort  (cost=46.02..46.06 rows=14 width=40)
              Sort Key: b.id
              ->  Nested Loop Left Join  (cost=9.03..45.76 rows=14 width=40)
                    ->  Bitmap Heap Scan on battle b  (cost=8.61..19.89 rows=3 width=36)
                          Recheck Cond: ((char1_id = 1) OR (char2_id = 1))
                          ->  BitmapOr  (cost=8.61..8.61 rows=3 width=0)
                                ->  Bitmap Index Scan on battle_char1_id_idx  (cost=0.00..4.30 rows=2 width=0)
                                      Index Cond: (char1_id = 1)
                                ->  Bitmap Index Scan on battle_char2_id_idx  (cost=0.00..4.30 rows=2 width=0)
                                      Index Cond: (char2_id = 1)
                    ->  Index Scan using battle_votes_battle_id_idx on battle_votes bv  (cost=0.42..8.55 rows=7 width=8)
                          Index Cond: (battle_id = b.id)

And with these simple changes we’ve reduced the cost of this query from 5664.53 to 46.26, a hundredth of the original! This is more in-line with the expectations for the speed of a search, especially now that it’s been optimized.

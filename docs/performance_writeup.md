# Fake Data Modeling
## Code

```uv run simulate.py```

The Code for each section is under src/simulate

## Estimated Total Rows
This is taken from simulate.py

```bash
user_total = 200,000
franchise_total = 1,000
character_total = 150,000 = 50,000 * 3 average franchises per character
review_total = 400,000 = 200,000 * 2 (franchise and character reviews)
battle_total = 250,000 = 50,000 * 5 (average votes per battle)
Total estimated rows ~ 1,000,000
```

We believe the database will scale where the majority of the database is comprised of Users. Frachises won't have as many as there are only so many popular franchises, however we included the possibility of people creating lesser known franchises or custom ones. With 200,000 users, we estimate that its possible to reach 1,000 franchises. Furthermore, we don't expect every user to be creating characters as the majority of users will scroll and look at other users comments/reviews. However, with 150,000 users, some might create multiple comments while others make none, which is why we estimated a total of 50,000 characters being created. This is quite a lot even still as that means its an average of 50 characters per franchise. However, duplicate characters can exist as users have the freedom to determine the stats of the characters. Since characters can be assigned multiple franchises, we imagine some users would want to create characters that are involved in multiple franchises due to parody or their own custom franchise/characters made with friends. We estimate that on average a user would create 2 reviews each. The simulated data does an even split of characters/franchises, which we don't expect to happen in practice, but for the sake of testing the efficiency of endpoints we decided to implement that split. Once again, not every user will create reviews, but the more active ones could potentially create multiple upwards to hundreds of reviews, while the majority of user will browse the content. Lastly the battles are a secondary source of our project with the main focus being the database of characters franchises. With that being said, we estimate the amount of battles to be less than the reviews as most people probably won't actually care too much about some silly online battle system with unregulated character stats. However, since they are so easy to create and vote upon, we imagine there will be a decent following from active individuals allowing for a solid on average 1 battle for every 4 users. Voting is created to be 0-10 scale in the simulated data, with it being 5 on average, resulting in 250,000 total rows.

# Performance Results of Hitting Endpoints

## Endpoint 1
GET /character/by_id/{character_id}
```
Description:
Get character by ID.
Runtime: (ms)
0.005954s
```

## Endpoint 2
GET /character/list/{user_id}
```
Description:
Get all characters made by user.
Runtime:
0.010645s
```

## Endpoint 3
GET /character/leaderboard
```
Description:
Get the leaderboard of characters.
Runtime:
0.019709s
```

## Endpoint 4
POST /character/make
```
Description:
Create a new character.
Runtime:
0.007769s
```

## Endpoint 5
GET /character/franchise/{character_id}
```
Description:
Get all franchises for a given character referencing its id.
Runtime:
0.014095s
```

## Endpoint 6
GET /franchise/by_id/{franchise_id}
```
Description:
Get franchise by ID.
Runtime:
0.005117s
```

## Endpoint 7
GET /franchise/by_name/{franchise_name}
```
Description:
Get franchise by name.
Runtime:
0.005311s
```

## Endpoint 8
POST /franchise/make
```
Description:
Create a new franchise.
Runtime:
0.006875s
```

## Endpoint 9
GET /user/by_id/{user_id}
```
Description:
Get User by ID.
Runtime:
0.005451s
```

## Endpoint 10
GET /user/by_name/{username}
```
Description:
Get User by name.
Runtime: 
0.006681s
```

## Endpoint 11
POST /user/make
```
Description:
Make a new user.
Runtime: 
0.007802s
```

## Endpoint 12
POST /user/favorite/character
```
Description:
Sets a user's favorite character.
Runtime:
0.011942s
```

## Endpoint 13
GET /user/favorite/character
```
Description:
Gets a user's favorite character and franchise.
Runtime:
0.005775s
```

## Endpoint 14
POST /user/favorite/franchise
```
Description:
Sets a user's favorite franchise.
Runtime:
0.010281s
```

## Endpoint 15
POST /review/character/create
```
Description:
Review a character.
Runtime:
0.012631s
```

## Endpoint 16
GET /review/character/list/{character_id}
```
Description:
Get all reviews for a given character referencing its id.
Runtime:
0.012530s
```

## Endpoint 17
POST /review/franchise/create
```
Description:
Make a review for a franchise.
Runtime:
0.012312s
```

## Endpoint 18
GET /review/franchise/list/{franchise_id}
```
Description:
Get all reviews for a given franchise referencing its id.
Runtime:
0.008459s
```

## Endpoint 19 (Third Slowest)
GET /battle/battle/{battle_id}
```
Description:
Get the result of a battle by its ID.
Runtime:
0.024302s
```

## Endpoint 20 (Slowest)
GET /battle/character/{character_id}/{page_id}
```
Description:
Get a list of battles a character has fought in.
Runtime:
0.042538s
```

## Endpoint 21 (Second Slowest)
GET /battle/user/{user_id}/{page_id}
```
Description:
Get a list of battles a user has participated in.
Runtime:
0.036662s
```

## Endpoint 22
POST /battle/vote/{user_id}/{battle_id}/{character_id}
```
Description:
Vote for a character during an active battle.
Runtime:
0.008979s
```

## Endpoint 23
POST /battle/make
```
Description:
Create a battle between two characters and return its id.
Runtime:
0.008245s
```

# Performance Tuning

## Initial Test
Our slowest endpoint was GET /battle/character/{character_id}. This was surprising because this endpoint only has one query, and isn’t as technically complex as some of the others. It should just list some battles following a parameter, right?

Upon running:
```bash
EXPLAIN ANALYZE SELECT *
FROM battle_with_votes
WHERE char1_id = 1 OR char2_id = 1
LIMIT 10 OFFSET 0
```

We got:
```
Limit  (cost=22607.48..22609.25 rows=6 width=52) (actual time=501.727..509.134 rows=2 loops=1)
  ->  Finalize GroupAggregate  (cost=22607.48..22609.25 rows=6 width=52) (actual time=501.725..509.132 rows=2 loops=1)
        Group Key: b.id
        ->  Gather Merge  (cost=22607.48..22609.10 rows=12 width=52) (actual time=501.716..509.121 rows=3 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Partial GroupAggregate  (cost=21607.46..21607.70 rows=6 width=52) (actual time=482.766..482.770 rows=1 loops=3)
                    Group Key: b.id
                    ->  Sort  (cost=21607.46..21607.49 rows=12 width=40) (actual time=482.756..482.759 rows=1 loops=3)
                          Sort Key: b.id
                          Sort Method: quicksort  Memory: 25kB
                          Worker 0:  Sort Method: quicksort  Memory: 25kB
                          Worker 1:  Sort Method: quicksort  Memory: 25kB
                          ->  Parallel Hash Right Join  (cost=5148.09..21607.24 rows=12 width=40) (actual time=271.827..482.016 rows=1 loops=3)
                                Hash Cond: (bv.battle_id = b.id)
                                ->  Parallel Seq Scan on battle_votes bv  (cost=0.00..14911.34 rows=589634 width=8) (actual time=0.258..269.839 rows=471707 loops=3)
                                ->  Parallel Hash  (cost=5148.04..5148.04 rows=4 width=36) (actual time=142.895..142.896 rows=1 loops=3)
                                      Buckets: 1024  Batches: 1  Memory Usage: 72kB
                                      ->  Parallel Seq Scan on battle b  (cost=0.00..5148.04 rows=4 width=36) (actual time=72.306..142.619 rows=1 loops=3)
                                            Filter: ((char1_id = 1) OR (char2_id = 2))
                                            Rows Removed by Filter: 99999
Planning Time: 2.957 ms
Execution Time: 510.540 ms
```

## First Indexing Tweak

The key thing that drives up the cost as the program searches the list is the right join on the ‘battle_vote’ table with the ‘battle’ table. The condition is a comprehensive search for any matches between the two id’s which means that the query ends up scanning all of the battle_vote rows because battle_id isn’t unique or indexed (yet!). 

Therefore, in order to improve the efficiency of this join and not have to scan all of the rows for matches, we just need to add an index to battle_id. This will make it easier to reference and join without scanning every row.

So, we created the following index:
```bash
CREATE INDEX ON battle_votes(battle_id);
```

Then, running the same explain query got us this:
```bash
Limit  (cost=6182.86..6183.94 rows=6 width=52) (actual time=32.543..36.405 rows=2 loops=1)
  ->  Finalize GroupAggregate  (cost=6182.86..6183.94 rows=6 width=52) (actual time=32.541..36.401 rows=2 loops=1)
        Group Key: b.id
        ->  Gather Merge  (cost=6182.86..6183.83 rows=6 width=52) (actual time=32.529..36.391 rows=2 loops=1)
              Workers Planned: 1
              Workers Launched: 1
              ->  Partial GroupAggregate  (cost=5182.85..5183.15 rows=6 width=52) (actual time=27.431..27.435 rows=1 loops=2)
                    Group Key: b.id
                    ->  Sort  (cost=5182.85..5182.89 rows=16 width=40) (actual time=27.421..27.424 rows=2 loops=2)
                          Sort Key: b.id
                          Sort Method: quicksort  Memory: 25kB
                          Worker 0:  Sort Method: quicksort  Memory: 25kB
                          ->  Nested Loop Left Join  (cost=0.43..5182.53 rows=16 width=40) (actual time=12.406..27.399 rows=2 loops=2)
                                ->  Parallel Seq Scan on battle b  (cost=0.00..5148.04 rows=4 width=36) (actual time=12.312..26.950 rows=1 loops=2)
                                      Filter: ((char1_id = 1) OR (char2_id = 2))
                                      Rows Removed by Filter: 149998
                                ->  Index Scan using battle_votes_battle_id_idx on battle_votes bv  (cost=0.43..8.55 rows=7 width=8) (actual time=0.398..0.401 rows=2 loops=2)
                                      Index Cond: (battle_id = b.id)
Planning Time: 2.592 ms
Execution Time: 36.539 ms
```

Pretty much all of the cost of that join has been lost since we added the index. Because iterating through battle_votes was so expensive, this change has cut our overall cost to run into a fifth of what it used to be!

## But It Can Be Better!

To take it one step further, we also realized that the sequential scan for the character ids within battle is expensive, though to a lesser degree. The character ids aren’t unique, so it makes sense that any query would have to search through the entire table to find what it was looking for. Therefore, a way to further optimize the query would be to make two more indexes, on char1_id and char2_id. Here’s the code we used to create them:

```bash
CREATE INDEX ON battle(char1_id);
CREATE INDEX ON battle(char2_id);
```

Re-running explain:
```bash
Limit  (cost=84.50..84.98 rows=6 width=52) (actual time=1.689..1.694 rows=2 loops=1)
  ->  GroupAggregate  (cost=84.50..84.98 rows=6 width=52) (actual time=1.688..1.692 rows=2 loops=1)
        Group Key: b.id
        ->  Sort  (cost=84.50..84.57 rows=28 width=40) (actual time=1.680..1.682 rows=4 loops=1)
              Sort Key: b.id
              Sort Method: quicksort  Memory: 25kB
              ->  Nested Loop Left Join  (cost=9.32..83.83 rows=28 width=40) (actual time=1.656..1.672 rows=4 loops=1)
                    ->  Bitmap Heap Scan on battle b  (cost=8.89..32.10 rows=6 width=36) (actual time=1.639..1.643 rows=2 loops=1)
                          Recheck Cond: ((char1_id = 1) OR (char2_id = 2))
                          Heap Blocks: exact=2
                          ->  BitmapOr  (cost=8.89..8.89 rows=6 width=0) (actual time=1.594..1.595 rows=0 loops=1)
                                ->  Bitmap Index Scan on battle_char1_id_idx  (cost=0.00..4.45 rows=3 width=0) (actual time=0.476..0.477 rows=0 loops=1)
                                      Index Cond: (char1_id = 1)
                                ->  Bitmap Index Scan on battle_char2_id_idx  (cost=0.00..4.45 rows=3 width=0) (actual time=1.091..1.091 rows=2 loops=1)
                                      Index Cond: (char2_id = 2)
                    ->  Index Scan using battle_votes_battle_id_idx on battle_votes bv  (cost=0.43..8.55 rows=7 width=8) (actual time=0.009..0.011 rows=2 loops=2)
                          Index Cond: (battle_id = b.id)
Planning Time: 1.916 ms
Execution Time: 1.781 ms
```

And with these simple changes we’ve reduced the cost of this query from 22609.25 to 84.98, a hundredth of the original or in other words, nearly a 266 times improvement in cost just by using index! Additionally the time to utilize this query is reduced from 509.134 ms to 1.694 ms, which is a 300 times improvement in the estaimted time. This is more in-line with the expectations for the speed of a search, especially now that it’s been optimized. 

## Additional Information and Improvements

While we only focused on endpoint 20, both endpoints 21 (second slowest) and 19 (third slowest) both suffer from similar query issues, we could do a similar improvement to those endpoints as well. The sequential scan for the user ids for endpoint 21 within users is expensive, so one improvement for addressing the cost in querying for this would be also indexing for users here. So adding one more index could potentially improve the time it takes to query. Additionally, endpoint 19 benefits from the changes at endpoint 20, where it would have to search a battle based on the battle id. Because we are indexing the battle id, the change here would also improve the time it takes to search for individual battle ids, and thus reduce the time taken to query for that.

### Three More Example Flows

Example Flow 4
Fan Fiction World-Building

Wendy the Writer is writing a fan fiction universe that combines characters from multiple fandoms in a single story. She's looking to build believable interactions and epic fights between characters, but struggles with consistency and balancing. She uses the Fictional Character Brawl to research characters and simulate encounters that will guide her story.

First, Nina calls GET /franchise/{franchise_id} narrow it down to character from "My Hero Academia" and "Attack on Titan" and see if the franchise exists

She selects "Levi Ackerman" and "Izuku Midoriya" using GET /character/{character_id} to learn about their attributes.

To check if their battle would be interesting, she submits them to POST /battle/make with a 7 day timer.

She uses GET /battle/{battle_id} to review the battle result and gets insights from the outcome and community comments after she 7 days.

She incorporates the battle dynamics into her writing, crafting an engaging scene for characters inspiried by these franchises.

Example Flow 5
Game Balance Tuning for an Indie Dev

Mark the Maker is an indie game developer balancing a PvP game where players can import characters inspired by fictional universes. His players complain about some characters being overpowered. Mark decides to use the Fictional Character Brawl to compare win rates and user sentiment to rebalance them.

Mark queries GET /character/leaderboard to see which characters are dominating win-wise.

He identifies two problematic characters: "Carrie Carry" and "Big Blade" and inspects their stats using GET /character/{character_id}.

To get community sentiment, he calls GET /character/reviews/{character_id} and looks at the feedback on "Big Blade".

He uses POST /battle/characters/{character_1}/{character_2} to simulate "Carrie Carry" vs "Big Blade" for 7 days.

After analyzing the win/loss balance and reviews, he tweaks their in-game stats and uses GET /battle/{battle_id} to see the winner after a week

Satisfied with the new balance, he updates his game with a new patch.

Example Flow 6
Cosplay Competition Inspiration

Jerry the Joker is a professional cosplayer preparing for a themed tournament where participants must portray characters with combat backgrounds. The contest judges creativity and character relevance. Jerry wants to impress by selecting a character who is both popular and has a strong win record.

He starts with GET /character/leaderboard to find highly ranked characters with frequent wins.

He notices "The Joker" from the Batman series and retrieves his details using GET /character/{character_id}.

Curious about matchups, he runs POST /battle/characters/{The Joker}/{Batman} to see how his choice performs against another stylish character.

He reads user reviews with GET /character/reviews/{The Joker} to understand the appeal and gather roleplaying tips.

Once users vote on the battle, he settles on The Joker, he leaves his own review using POST /character/review/{The Joker} to engage with the community.

He uses the insights and battle data to determine that he will cosplay as the Joker.

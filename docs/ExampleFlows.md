<h1>Example Flows</h1>

<p>Project Members: Adam Kong, Brian Kaplan, Vic Grigoryev</p>

<h5>Cal Poly Email: aakong@calpoly.edu, bhkaplan@calpoly.edu, vgrigory@calpoly.edu</h5>

<h3>Example Flow 1</h3>

<h4>Character Battle Exploration Example</h4>

Chad a content creator who goes under the name _Chad Battles!_ is heavily inspiried by the ideas of the _Death Battle!_ series on Youtube. He is so inspiried that he wants to create his own DeathBattle series but has no idea how to begin or where to start. But he does know that he needs two characters and loves the franchise of _Dragon Ball Z_ and _Fornite_. He first request the franchises of both _Dragon Ball Z_ and _Fortnite_ and sees that there are two character ids he wants. He wants to use character id with "Goku/Kakorot" and "Jonesy". He then takes both ids and reviews their information before casting his own review and voting on the character and finally gets places the two characters to fight against each other and creatively akes his video to post on to Youtube.

Chad starts this process by

- starts by calling GET /franchise/{franchise_id} with "Dragon Ball Z" and "Fortnite"
- then he calls GET /character/{character_id} with "Goku/Kakorot" and "Jonesy"
- reviews both of them with POST /character/review/{character_id} with "Goku/Kakorot" and "Jonesy"
- finally he battles and gets results with them with POST /battle/characters/{character_1}/{character_2} with "Goku/Kakorot" and "Jonesy"

Chad continues with his video, using a simulated battle and community feedback on the matchup.

<h3>Example Flow 2</h3>

<h4>Character Creation Process</h4>

Gary Monster is a Game Master for his local D&D club and manages several boards. He is relatively new to making new foes and characters. Many players are complaining about the power scaling and unfair matchup between their characters and the monsters and Gary is facing the ultimately problem of scaling. He looks on online forums like _Reddit_ but found it was hard to navigate and get consistent answer for match ups. He then looked at the API for potential new data that users can place their input in and vote on characters and reviews. He found that this would solve his problem of power sclaing as users would be similar to the players and himself.

Gary begins by
- placing all his created enemies and player stats into POST /character/make/{user_id}/{character_id} to find a balance. In this case he uses two characters an enemy "Goblin_1" and a players character "Perry_the_Paladin"
- Eventually he goes to POST /battle/characters/{character_1}/{character_2} to matchup certain enemies he's worried about when they have a large number of wins. For example he uses "Goblin_1" and a players character "Perry_the_Paladin"
- He looks at critques and comments users had about his characters with POST /character/review/{character_id} for his charcter of "Goblin_1"

Finally Gary goes off and is able to make balanced characters because of the changes the battles suggested to him

<h3>Example Flow 3</h3>

<h4>Online Debate Lookup</h4>

Roxy the Rager and Danny the Debater are known online for having the strongest opposing debates with characters. They both constantly look up leaderboards online to find which character does the best. One day Danny wants to completely win the debate once and for all, and looks up Roxy user information to find out between him and her who has the most wins and gets battles right more.

Danny starts his investigtion by
- finding the current leaderboard with GET /character/leaderboard
- he finds the current top chracters and is happy to see most of his characters is agreed to be on top, he then searches with GET /battle/user/{user_id} using Roxy_the_rager
- He's happy to see the trend of losses on her profile then searches her characters with GET /character/{user_id} using Roxy_the_rager
- He then places his top character with her top character using POST /battle/characters/{character_1}/{character_2} using Roxy_Runner and Danny_The_Destroyer

He then gather all this data to present to her in a more fashion debate until the cycle returns again.

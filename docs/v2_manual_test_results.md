<h1>Example Flows</h1>

<h3>Example Flow 1</h3>

<h4>Character Battle Exploration Example</h4>

Chad a content creator who goes under the name _Chad Battles!_ is heavily inspiried by the ideas of the _Death Battle!_ series on Youtube. He is so inspiried that he wants to create his own DeathBattle series but has no idea how to begin or where to start. But he does know that he needs two characters and loves the franchise of _Dragon Ball Z_ and _Fornite_. He first request the franchises of both _Dragon Ball Z_ and _Fortnite_ and sees that there are two character ids he wants. He wants to use character id with "Goku/Kakorot" and "Jonesy". He then takes both ids and reviews their information before casting his own review and voting on the character and finally gets places the two characters to fight against each other and creatively akes his video to post on to Youtube.

Chad starts this process by

- starts by calling GET /franchise/{franchise_id} with "Dragon Ball Z" and "Fortnite"
- then he calls GET /character/{character_id} with "Goku/Kakorot" and "Jonesy"
- reviews both of them with POST /character/review/{character_id} with "Goku/Kakorot" and "Jonesy"
- finally he battles and gets results with them with POST /battle/characters/{character_1}/{character_2} with "Goku/Kakorot" and "Jonesy"

Chad continues with his video, using a simulated battle and community feedback on the matchup.

<h3>Testing Results 1</h3>

Curl Statements:
curl -X 'GET' \
  'http://127.0.0.1:8000/franchise/get/by_name/Dragon%20Ball%20Z' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8000/franchise/get/by_name/Fortnite' \
  -H 'accept: application/json'

Responses:
{
  "id": 1,
  "name": "Dragon Ball Z",
  "description": "Like Dragon Ball, but we used letters A-Y already"
}

{
  "id": 2,
  "name": "Fortnite",
  "description": "The King of Collabs"
}

Curl Statements:
curl -X 'GET' \
  'http://127.0.0.1:8000/character/get/by_name/Goku' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8000/character/get/by_name/Jonesy' \
  -H 'accept: application/json'

Responses:
{
  "char_id": 5,
  "user_id": 1,
  "name": "Goku",
  "description": "I don't know who this Kakarot guy is, he's not me",
  "rating": 0,
  "strength": 150000000,
  "speed": 600,
  "health": 3000
}

{
  "char_id": 4,
  "user_id": 1,
  "name": "Jonesy",
  "description": "Gives me bacon cheeseburger vibes",
  "rating": 0,
  "strength": 10,
  "speed": 20,
  "health": 100

Curl Statements:
curl -X 'POST' \
  'http://127.0.0.1:8000/character/review/{char_id}?user_id=1&character_id=5&comment=Too%20OP%21' \
  -H 'accept: */*' \
  -d ''

curl -X 'POST' \
  'http://127.0.0.1:8000/character/review/{char_id}?user_id=1&character_id=4&comment=Add%20tac%20smg%20pls' \
  -H 'accept: */*' \
  -d ''

Responses: N/A

Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/battle/make' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "char1_id": 5,
  "char2_id": 4,
  "duration": 24
}'

Response:
{
  "battle_id": 4,
  "char1_id": 5,
  "char2_id": 5,
  "duration": 24,
  "start": "2025-05-12T20:15:05.476578",
  "end": "2025-05-13T20:15:05.476578"
}

<h3>Example Flow 2</h3>

<h4>Character Creation Process</h4>

Gary Monster is a Game Master for his local D&D club and manages several boards. He is relatively new to making new foes and characters. Many players are complaining about the power scaling and unfair matchup between their characters and the monsters and Gary is facing the ultimately problem of scaling. He looks on online forums like _Reddit_ but found it was hard to navigate and get consistent answer for match ups. He then looked at the API for potential new data that users can place their input in and vote on characters and reviews. He found that this would solve his problem of power sclaing as users would be similar to the players and himself.

Gary begins by
- placing all his created enemies and player stats into POST /character/make/{user_id}/{character_id} to find a balance. In this case he uses two characters an enemy "Goblin_1" and a players character "Perry_the_Paladin"
- Eventually he goes to POST /battle/characters/{character_1}/{character_2} to matchup certain enemies he's worried about when they have a large number of wins. For example he uses "Goblin_1" and a players character "Perry_the_Paladin"
- He looks at critques and comments users had about his characters with POST /character/review/{character_id} for his charcter of "Goblin_1"

Finally Gary goes off and is able to make balanced characters because of the changes the battles suggested to him

<h3>Testing Results 2</h3>

Curl Statements:
curl -X 'POST' \
  'http://127.0.0.1:8000/character/make?user_id=4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "character": {
    "name": "Goblin_1",
    "description": "no comment, just a widdle gobwin",
    "strength": 1,
    "speed": 7,
    "health": 3
  },
  "franchiselist": []
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/character/make?user_id=4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "character": {
    "name": "Perry the Paladin",
    "description": "Has a pet platypus of the same name.",
    "strength": 4,
    "speed": 2,
    "health": 10
  },
  "franchiselist": []
}'

Responses:
{
  "char_id": 6,
  "user_id": 4,
  "name": "Goblin_1",
  "description": "no comment, just a widdle gobwin",
  "rating": 0,
  "strength": 1,
  "speed": 7,
  "health": 3
}

{
  "char_id": 7,
  "user_id": 4,
  "name": "Perry the Paladin",
  "description": "Has a pet platypus of the same name.",
  "rating": 0,
  "strength": 4,
  "speed": 2,
  "health": 10
}

Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/battle/make' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 4,
  "char1_id": 6,
  "char2_id": 7,
  "duration": 12
}'

Response:
{
  "battle_id": 5,
  "char1_id": 6,
  "char2_id": 6,
  "duration": 12,
  "start": "2025-05-12T20:23:04.588552",
  "end": "2025-05-13T08:23:04.588552"
}

Curl Statement:
curl -X 'GET' \
  'http://127.0.0.1:8000/character/get_review/6' \
  -H 'accept: application/json'

Response:
[
  {
    "user_id": 1,
    "comment": "Five stars from Frank!!"
  },
  {
    "user_id": 4,
    "comment": "Kinda speedy, really only wins vs things with 1 hp"
  }
]

<h3>Example Flow 3</h3>

<h4>Online Debate Lookup</h4>

Roxy the Rager and Danny the Debater are known online for having the strongest opposing debates with characters. They both constantly look up leaderboards online to find which character does the best. One day Danny wants to completely win the debate once and for all, and looks up Roxy user information to find out between him and her who has the most wins and gets battles right more.

Danny starts his investigtion by
- finding the current leaderboard with GET /character/leaderboard, finding the current top characters.
- searching for Roxy's user id by calling GET /user/get/by_name/{username} and passing in her username, Roxystarr.
- pulling up a record of all of Roxy's battles with GET /battle/user/{user_id} using her user id.
- then searching her characters with GET /character/{user_id} using Roxy_the_rager (Danny'll also search up all of his characters for good measure)
- matching up his top character with her top character using POST /battle/characters/{character_1}/{character_2} using Tigrimm the Dream-Eater and Bassilisk

He then gather all this data to present to her in a more fashion debate until the cycle returns again.

<h3>Testing Results 3</h3>

Curl Statement:
curl -X 'GET' \
  'http://127.0.0.1:8000/character/leaderboard' \
  -H 'accept: application/json'

Response:
[
  {
    "char_id": 2,
    "user_id": 1,
    "name": "DJ Heartbeats",
    "description": "Probably the coolest DJ ever, but only performs on Valentine's Day.",
    "rating": 0,
    "strength": 1,
    "speed": 6,
    "health": 50
  },
  {
    "char_id": 4,
    "user_id": 1,
    "name": "Jonesy",
    "description": "Gives me bacon cheeseburger vibes",
    "rating": 0,
    "strength": 10,
    "speed": 20,
    "health": 100
  },
  {
    "char_id": 5,
    "user_id": 1,
    "name": "Goku",
    "description": "I don't know who this Kakarot guy is, he's not me",
    "rating": 0,
    "strength": 150000000,
    "speed": 600,
    "health": 3000
  },
  {
    "char_id": 6,
    "user_id": 4,
    "name": "Goblin_1",
    "description": "no comment, just a widdle gobwin",
    "rating": 0,
    "strength": 1,
    "speed": 7,
    "health": 3
  },
  {
    "char_id": 7,
    "user_id": 4,
    "name": "Perry the Paladin",
    "description": "Has a pet platypus of the same name.",
    "rating": 0,
    "strength": 4,
    "speed": 2,
    "health": 10
  },
  {
    "char_id": 8,
    "user_id": 5,
    "name": "Bassilisk",
    "description": "A serpentine beast whose subsonic gaze petrifies you mid-groove",
    "rating": 0,
    "strength": 5,
    "speed": 16,
    "health": 50
  },
  {
    "char_id": 9,
    "user_id": 5,
    "name": "Saxsquatch",
    "description": "Wields an otherworldly tool of sweet destruction, the saxophone",
    "rating": 0,
    "strength": 13,
    "speed": 1,
    "health": 31
  },
  {
    "char_id": 10,
    "user_id": 6,
    "name": "Alex Yiik",
    "description": "The developer and main character of his own game. Truly peak.",
    "rating": 0,
    "strength": 1,
    "speed": 3,
    "health": 7
  },
  {
    "char_id": 11,
    "user_id": 6,
    "name": "Tigrimm the Dream-Eater",
    "description": "A planar beast who stalks nightmares, leaving behind clawed symbols burned into minds.",
    "rating": 0,
    "strength": 9,
    "speed": 3,
    "health": 42
  }
]

Curl Statement:
curl -X 'GET' \
  'http://127.0.0.1:8000/user/get/by_name/Roxystarr' \
  -H 'accept: application/json'

Response:
{
  "id": 5,
  "name": "Roxystarr"
}

Curl Statement:
curl -X 'GET' \
  'http://127.0.0.1:8000/battle/get/user/5' \
  -H 'accept: application/json'

Response:
[
  {
    "battle_id": 6,
    "char1_id": 8,
    "char2_id": 9,
    "winner_id": 8,
    "start": "2025-05-12T20:56:33.229870",
    "end": "2025-05-13T01:56:33.229870",
    "finished": false
  },
  {
    "battle_id": 8,
    "char1_id": 9,
    "char2_id": 2,
    "winner_id": 9,
    "start": "2025-05-12T20:57:19.431330",
    "end": "2025-05-13T01:57:19.431330",
    "finished": false
  },
  {
    "battle_id": 7,
    "char1_id": 8,
    "char2_id": 4,
    "winner_id": 4,
    "start": "2025-05-12T20:57:00.475194",
    "end": "2025-05-13T01:57:00.475194",
    "finished": false
  }
]

Curl Statements:
curl -X 'GET' \
  'http://127.0.0.1:8000/character/list/5' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8000/character/list/6' \
  -H 'accept: application/json'

Responses:
[
  {
    "char_id": 8,
    "user_id": 5,
    "name": "Bassilisk",
    "description": "A serpentine beast whose subsonic gaze petrifies you mid-groove",
    "rating": 1,
    "strength": 5,
    "speed": 16,
    "health": 50
  },
  {
    "char_id": 9,
    "user_id": 5,
    "name": "Saxsquatch",
    "description": "Wields an otherworldly tool of sweet destruction, the saxophone",
    "rating": 1,
    "strength": 13,
    "speed": 1,
    "health": 31
  }
]

[
  {
    "char_id": 10,
    "user_id": 6,
    "name": "Alex Yiik",
    "description": "The developer and main character of his own game. Truly peak.",
    "rating": 0,
    "strength": 1,
    "speed": 3,
    "health": 7
  },
  {
    "char_id": 11,
    "user_id": 6,
    "name": "Tigrimm the Dream-Eater",
    "description": "A planar beast who stalks nightmares, leaving behind clawed symbols burned into minds.",
    "rating": 0,
    "strength": 9,
    "speed": 3,
    "health": 42
  }
]

Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/battle/make' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6,
  "char1_id": 11,
  "char2_id": 8,
  "duration": 2
}'

Response:
{
  "battle_id": 9,
  "char1_id": 11,
  "char2_id": 11,
  "duration": 2,
  "start": "2025-05-12T21:40:51.801835",
  "end": "2025-05-12T23:40:51.801835"
}

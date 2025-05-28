# Example workflow

<h4>Character Creation and Review</h4>

Five-Star Frank is a famous game character reviewer, but he has a secret: he likes to review his own original characters, and give them the highest reviews! Having heard of our database, he wants to upload his own character, DJ Heartbeats, and upload a review for it. Then, he will be able to fetch the review, show it to all of his associates, and earn the adoring praise he always knew he deserved!

Frank would go about this by:

- first creating a new user by calling POST /user/make and passing in his username, "StarStarStarStarStar" as a parameter
- next using that user to create a character by calling POST /character/make and passing in his user_id and the name and details of DJ Heartbeats into the request body.
- then writing a review by calling POST /character/review/{char_id}, passing in his user id, character id, and his description text highlighting DJ Heartbeats unparalleled health stat.
- finally fetching all of DJ Heartbeats' reviews with GET /character/get_review/{char_id} and passing in the character id

Now, Frank can see his review for his character, and is filled with a surge of pride upon reading the review.

# Testing results

Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/user/make?name=StarStarStarStarStar' \
  -H 'accept: application/json' \
  -d ''

Response:
{
  "id": 0,
  "name": "string"
}


Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/character/make?user_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "DJ Heartbeats",
  "description": "Probably the coolest DJ ever, but only performs on Valentine'\''s Day.",
  "rating": 0,
  "strength": 1,
  "speed": 6,
  "health": 50
}'

Response:
{
  "char_id": 2,
  "user_id": 1,
  "name": "DJ Heartbeats",
  "description": "Probably the coolest DJ ever, but only performs on Valentine's Day.",
  "rating": 0,
  "strength": 1,
  "speed": 6,
  "health": 50
}


Curl Statement:
curl -X 'POST' \
  'http://127.0.0.1:8000/character/review/{char_id}?user_id=1&character_id=2&comment=Five%20Stars%21%21%20I%20am%20not%20Frank%2C%20but%20I%20am%20a%20big%20fan%20of%20him%2C%20his%20characters%2C%20and%20his%20reviews%21' \
  -H 'accept: */*' \
  -d ''

Response:
This endpoint does not have a response as of right now.


Curl Statement:
curl -X 'GET' \
  'http://127.0.0.1:8000/character/get_review/2' \
  -H 'accept: application/json'

Response:
[
  {
    "user_id": 1,
    "comment": "Five Stars!! I am not Frank, but I am a big fan of him, his characters, and his reviews!"
  }
]

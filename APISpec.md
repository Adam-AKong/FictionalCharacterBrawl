<h1>API Specifications</h1>

<p>Project Members: Adam Kong, Brian Kaplan, Vic Grigoryev, William Pierce</p>

<h5>Cal Poly Email: aakong@calpoly.edu, bhkaplan@calpoly.edu, vgrigory@calpoly.edu, wqpierce@calpoly.edu</h5>

<h3> Endpoint 1</h3>

## GET /character/by_id/{character_id}

**Description:**  
Get character by ID.

**Response Example:**

```json
{
  "char_id": 0,
  "user_id": 0,
  "name": "string",
  "description": "string",
  "rating": 0,
  "strength": 0,
  "speed": 0,
  "health": 0
}
```
<h3> Endpoint 2</h3>

## GET /character/list/{user_id}

**Description:**  
Get all characters made by user.

**Response Example:**

```json
[
  {
    "char_id": 0,
    "user_id": 0,
    "name": "string",
    "description": "string",
    "rating": 0,
    "strength": 0,
    "speed": 0,
    "health": 0
  }
]
```
<h3> Endpoint 3</h3>

## GET /character/leaderboard

**Description:**
Get the leaderboard of characters.

**Response Example:**

```json
[
  {
    "char_id": 0,
    "user_id": 0,
    "name": "string",
    "description": "string",
    "rating": 0,
    "strength": 0,
    "speed": 0,
    "health": 0
  }
]
```
<h3> Endpoint 4</h3>

## POST /character/make

**Description:**
Create a new character.

**Response Example:**

```json
{
  "character": {
    "name": "string",
    "description": "string",
    "strength": 0,
    "speed": 0,
    "health": 0
  },
  "franchiselist": [
    {
      "franchise_id": 0
    }
  ]
}
```
<h3> Endpoint 5</h3>

## GET /character/franchise/{character_id}

**Description:**
Get all franchises for a given character referencing its id.

**Response Example:**

```json
[
  {
    "id": 0,
    "name": "string",
    "description": "string"
  }
]
```
<h3> Endpoint 6</h3>

## GET /franchise/by_id/{franchise_id}

**Description:**
Get franchise by ID.

**Response Example:**

```json
{
  "id": 0,
  "name": "string",
  "description": "string"
}
```
<h3> Endpoint 7</h3>

## GET /franchise/by_name/{franchise_name}

**Description:**
Get franchise by name.

**Response Example:**

```json
{
  "id": 0,
  "name": "string",
  "description": "string"
}
```
<h3> Endpoint 8</h3>

## POST /franchise/make

**Description:**
Create a new franchise.

**Response Example:**

```json
{
  "id": 0,
  "name": "string",
  "description": "string"
}
```
<h3> Endpoint 9</h3>

## GET /user/by_id/{user_id}

**Description:**  
Get User by ID.

**Response Example:**

```json
{
  "id": 0,
  "name": "string"
}
```
<h3> Endpoint 10</h3>

## GET /user/by_name/{username}

**Description:**  
Get User by name.

**Response Example:**

```json
{
  "id": 0,
  "name": "string"
}
```
<h3> Endpoint 11</h3>

## POST /user/make

**Description:**  
Make a new user.

**Response Example:**

```json
{
  "id": 0,
  "name": "string"
}
```
<h3> Endpoint 12</h3>

## POST /user/favorite/character

**Description:**  
Sets a user's favorite character.

**Response Example:**

```json
"Favorite character was set"
```
<h3> Endpoint 13</h3>

## GET /user/favorite/character

**Description:**  
Gets a user's favorite character and franchise.

**Response Example:**

```json
{
  "favorite_character_id": 0,
  "favorite_franchise_id": 0
}
```
<h3> Endpoint 14</h3>

## POST /user/favorite/franchise

**Description:**  
Sets a user's favorite franchise.

**Response Example:**

```json
"Favorite franchise was set"
```
<h3> Endpoint 15</h3>

## POST /review/character/create

**Description:**  
Review a character.

**Response Example:**

```json
{
  "user_id": 0,
  "char_id": 0,
  "comment": "string"
}
```
<h3> Endpoint 16</h3>

## GET /review/character/list/{character_id}

**Description:**  
Get all reviews for a given character referencing its id.

**Response Example:**

```json
[
  {
    "user_id": 0,
    "char_id": 0,
    "comment": "string"
  }
]
```
<h3> Endpoint 17</h3>

## POST /review/franchise/create

**Description:**  
Make a review for a franchise.

**Response Example:**

```json
{
  "user_id": 0,
  "fran_id": 0,
  "comment": "string"
}
```
<h3> Endpoint 18</h3>

## GET /review/franchise/list/{franchise_id}

**Description:**  
Get all reviews for a given franchise referencing its id.

**Response Example:**

```json
[
  {
    "user_id": 0,
    "fran_id": 0,
    "comment": "string"
  }
]
```
<h3> Endpoint 19</h3>

## GET /battle/battle/{battle_id}

**Description:**  
Get the result of a battle by its ID.

**Response Example:**

```json
{
  "battle_id": 0,
  "user_id": 0,
  "char1_id": 0,
  "char2_id": 0,
  "winner_id": 0,
  "start": "2025-05-28T02:28:36.275Z",
  "end": "2025-05-28T02:28:36.275Z",
  "finished": true
}
```
<h3> Endpoint 20</h3>

## GET /battle/character/{character_id}

**Description:**  
Get a list of battles a character has fought in.

**Response Example:**

```json
[
  {
    "battle_id": 0,
    "user_id": 0,
    "char1_id": 0,
    "char2_id": 0,
    "winner_id": 0,
    "start": "2025-05-28T02:28:58.198Z",
    "end": "2025-05-28T02:28:58.198Z",
    "finished": true
  }
]
```
<h3> Endpoint 21</h3>

## GET /battle/user/{user_id}

**Description:**  
Get a list of battles a user has participated in.

**Response Example:**

```json
[
  {
    "battle_id": 0,
    "user_id": 0,
    "char1_id": 0,
    "char2_id": 0,
    "winner_id": 0,
    "start": "2025-05-28T02:29:38.912Z",
    "end": "2025-05-28T02:29:38.912Z",
    "finished": true
  }
]
```
<h3> Endpoint 22</h3>

## POST /battle/vote/{user_id}/{battle_id}/{character_id}

**Description:**  
Vote for a character during an active battle.

**Response Example:**

```json
{
  "message": "string",
  "battle_id": 0,
  "char_id": 0
}
```
<h3> Endpoint 23</h3>

## POST /battle/make

**Description:**  
Create a battle between two characters and return its id.

**Response Example:**

```json
{
  "user_id": 0,
  "char1_id": 0,
  "char2_id": 0,
  "duration": 0
}
```

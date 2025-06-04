# Fictional Character Brawl
Hello, welcome to the Fictional Character Brawl. Here we want to ensure characters can be tested through battle with health, speed, and strength. We will create more developements as this project continues.

Group Members:
Brian Kaplan
Adam Kong
William Pierce
Vic Grigoryev

To run your server locally:

Install Dependencies

Install uv
Run:
```
uv sync
```
Setup local database

Run the following command in your terminal:

```
docker run --name mypostgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres:latest
```

*Note if you have a potion shop running on this port, you are most likely running on the default port. If you are run this instead

```
docker run --name mypostgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5440:5432 -d postgres:latest
```

Below run this if you are using this alternative port
```
postgresql://myuser:mypassword@localhost:5440/mydatabase
```

Upgrade the database to your latest schema:

```
uv run alembic upgrade head
```

Download and install TablePlus or DBeaver. Any SQL editor compatible with postgres will work.

Create a new connection with the following connection string:

```
postgresql://myuser:mypassword@localhost:5432/mydatabase
```
This will let you query your database and debug issues.

Run the Server

```
uv run main.py
```
Test Endpoints

Open http://127.0.0.1:3000/docs.
Use the interactive documentation to test API endpoints.
Run Tests

Write test cases in the tests/ folder.
Run tests with:
```
uv run pytest
```

# Fictional Character Brawl Database Setup

First we want to create the Fictional Character Brawl database. Run this command in your terminal:
docker run --name fcb -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword2 -e POSTGRES_DB=mydatabase -p 5433:5432 -d postgres:latest

* Note there is an alternative port if the 5433 is somehow polluted or not working which will be on the bottom. Replace 5433 in all the commands with 5440 instead.

Once the database is created on Docker go to table plus and run this into the table plus:
postgresql+psycopg://myuser:mypassword2@localhost:5433/mydatabase

After connecting the Docker and Tableplus together, run this command in the terminal:
docker start fcb

After Docker and Tableplus are successfully running, run this command in the terminal, which will bring the fastAPI and you will be able to change a local database
uvicorn main:app --reload

Now the app is developed and you will be able to test functionality.

from fastapi import FastAPI
from src.api import battle, character, franchise, user
from starlette.middleware.cors import CORSMiddleware

description = """
Premier Database for all your fictional character needs.
"""
tags_metadata = [
    {"name": "Battle", "description": "Create, vote, and view battles here."},
    {"name": "Character", "description": "Create characters with fun stats!"},
    {"name": "Franchise", "description": "Create franchises."},
    {"name": "User", "description": "Create new users."},
]

app = FastAPI(
    title="Fictional Character Brawl",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Adam Kong",
        "email": "aakong@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(battle.router)
app.include_router(character.router)
app.include_router(franchise.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Characters are waiting to brawl..."}

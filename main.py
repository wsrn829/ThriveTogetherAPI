from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# SessionLocal
# import os
from dotenv import load_dotenv


from authenticator import authenticator
from messages.routers import messages
from accounts.routers import accounts
from peers.routers import peers
from matching.routers import matching
from tags.routers import tags
from database import initialize_database, close_engine


load_dotenv()

app = FastAPI()

# db_engine = create_database_engine()

# initialize_database()

app.include_router(authenticator.router)
app.include_router(messages.messages_router)
app.include_router(accounts.router)
app.include_router(peers.router)
app.include_router(matching.router)
app.include_router(tags.router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=[
        "https://oyster-app-cxtg3.ondigitalocean.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "You hit the root path!"}


@app.on_event("startup")
async def startup():
    # app.db_connection = connect_to_db()
    initialize_database()


@app.on_event("shutdown")
async def shutdown():
    close_engine()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# async def get_database():
#     return app.db_connection


# @app.get("/api/launch-details")
# def launch_details():
#     return {
#         "launch_details": {
#             "module": 3,
#             "week": 17,
#             "day": 5,
#             "hour": 19,
#             "min": "00",
#         }
#     }

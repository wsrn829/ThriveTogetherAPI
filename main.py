from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# SessionLocal
import os
from dotenv import load_dotenv

# from authenticator import authenticator
from messages.routers import messages
from accounts.routers import accounts
from peers.routers import peers
from matching.routers import matching
from tags.routers import tags
from database import initialize_database

load_dotenv()

app = FastAPI()


# db_engine = create_database_engine()

initialize_database()

# app.include_router(authenticator.router)
app.include_router(messages.messages_router)
app.include_router(accounts.router)
app.include_router(peers.router)
app.include_router(matching.router)
app.include_router(tags.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.environ.get("CORS_HOST", "http://localhost:3000"),
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('PORT')


# db_config = {
#     'user': db_user,
#     'password': password,
#     'dbname': db_name,
#     'host': host
# }

# DATABASE_URL = f'postgresql://{db_user}:{password}@{host}:{port}/{db_name}'


# engine = create_engine(DATABASE_URL)

# # Bind the engine to the Base class
# UsersBase.metadata.create_all(engine)

# engine.dispose()

# MatchesBase.metadata.create_all(engine)

# engine.dispose()

# PeersBase.metadata.create_all(engine)

# engine.dispose()

# MessagesBase.metadata.create_all(engine)

# engine.dispose()

# UsersTagsBase.metadata.create_all(engine)

# engine.dispose()

# TagsBase.metadata.create_all(engine)


# Optional: Create a session
# Session = sessionmaker(bind=engine)
# session = Session()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def create_database_engine():
#     return create_engine(DATABASE_URI)


# @app.get("/")
# def root():
#     return {"message": "You hit the root path!"}


# @app.on_event("startup")
# async def startup():
#     app.db_connection = connect_to_db()


# @app.on_event("shutdown")
# async def shutdown():
#     close_connection(app.db_connection)


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

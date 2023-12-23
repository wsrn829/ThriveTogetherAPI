from pydantic import BaseModel


class AccountIn(BaseModel):
    username: str
    password: str
    name: str
    age: int
    gender: str
    pronouns: str
    email: str


class AccountOut(BaseModel):
    id: int
    username: str
    name: str
    age: int
    gender: str
    pronouns: str
    email: str
    profile_image: str | None
    banner_image: str | None
    about_me: str | None
    my_story: str | None
    preferences: str | None


class AccountOutWithPassword(AccountOut):
    hashed_password: str

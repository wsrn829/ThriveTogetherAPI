from pydantic import BaseModel


class HttpError(BaseModel):
    detail: str


class TagsOut(BaseModel):
    tags: list[str]


class MatchOut(BaseModel):
    username: str
    id: int
    tags: list[str]
    about_me: str | None
    profile_link: str | None
    profile_image: str | None
    gender: str
    pronouns: str


class MatchesOut(BaseModel):
    matches: list[MatchOut]

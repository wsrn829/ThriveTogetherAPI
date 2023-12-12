from pydantic import BaseModel


class HttpError(BaseModel):
    detail: str


class SuccessMessage(BaseModel):
    success: str


class TagsOut(BaseModel):
    tags: list[dict]


class AllTagsOut(BaseModel):
    tags: list[dict]


class Tag(BaseModel):
    tag: str

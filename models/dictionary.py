from pydantic import BaseModel


class DictionaryResponse(BaseModel):
    id: int
    letter: str
    image_url: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True

class DictionaryCreate(BaseModel):
    letter: str
    image_url: str | None = None
    description: str | None = None
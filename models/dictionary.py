from pydantic import BaseModel


class DictionaryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    image_url: str | None = None

    class Config:
        from_attributes = True


class DictionaryCreate(BaseModel):
    name: str
    description: str | None = None
    category: str
    image_url: str | None = None
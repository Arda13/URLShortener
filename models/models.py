from pydantic import BaseModel

class URL(BaseModel):
	url: str

class ShortURL(BaseModel):
	short_url: str
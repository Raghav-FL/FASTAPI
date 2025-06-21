from pydantic import BaseModel

class SampleItem(BaseModel):
    name: str
    value: int

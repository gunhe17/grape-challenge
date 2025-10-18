from pydantic import BaseModel
from typing import Any

class UsecaseOutput(BaseModel):
    content: Any
    code: int
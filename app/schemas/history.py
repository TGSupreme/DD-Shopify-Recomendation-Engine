from pydantic import BaseModel
from typing import List

class UserHistory(BaseModel):
    purchased: List[str] = []
    add_to_cart: List[str] = []
    viewed: List[str] = []

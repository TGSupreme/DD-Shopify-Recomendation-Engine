from pydantic import BaseModel
from typing import List

class UserHistory(BaseModel):
    store_id: str
    purchased: List[str] = []
    add_to_cart: List[str] = []
    viewed: List[str] = []

from typing import List
from app.domain.models import ShoppingList, ShoppingListCreate
from app.infrastructure import repo


def create_shopping_list(data: ShoppingListCreate) -> int:
    return repo.create_list(data)


def get_shopping_list(list_id: int) -> dict:
    return repo.get_list(list_id)

def list_shopping_lists() -> List[ShoppingList]:
    return repo.list_shopping_lists()
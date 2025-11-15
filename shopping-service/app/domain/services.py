from app.domain.models import ShoppingListCreate
from app.infrastructure import repo


def create_shopping_list(data: ShoppingListCreate) -> int:
    return repo.create_list(data)


def get_shopping_list(list_id: int) -> dict:
    return repo.get_list(list_id)
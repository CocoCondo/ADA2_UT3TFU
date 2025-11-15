from typing import List
from app.domain.models import Recipe, RecipeCreate, RecipeItemCreate
from app.infrastructure import repo


def create_recipe(data: RecipeCreate) -> Recipe:
    rid = repo.insert_recipe(data)
    return Recipe(id=rid, name=data.name, steps=data.steps)


def get_all_recipes() -> List[Recipe]:
    return repo.list_recipes()


def add_item(recipe_id: int, item: RecipeItemCreate) -> None:
    repo.add_recipe_item(recipe_id, item)
import json
from dataclasses import asdict
from pathlib import Path

from shopping_list.model import Item, ShoppingList


def load(path: Path) -> ShoppingList:
    if not path.exists():
        return ShoppingList()
    raw = json.loads(path.read_text())
    return ShoppingList(items=[Item(**item) for item in raw["items"]])


def save(shopping: ShoppingList, path: Path) -> None:
    data = {"items": [asdict(item) for item in shopping.items]}
    path.write_text(json.dumps(data, indent=2) + "\n")

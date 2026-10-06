from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    quantity: int = 1
    done: bool = False


@dataclass
class ShoppingList:
    items: list[Item] = field(default_factory=list)

    def add(self, name: str, quantity: int = 1) -> Item:
        name = name.strip()
        if not name:
            raise ValueError("item name must not be empty")
        if quantity < 1:
            raise ValueError("quantity must be at least 1")

        existing = self.find(name)
        if existing:
            existing.quantity += quantity
            return existing

        item = Item(name=name, quantity=quantity)
        self.items.append(item)
        return item

    def find(self, name: str) -> Item | None:
        wanted = name.strip().lower()
        return next((item for item in self.items if item.name.lower() == wanted), None)

    def mark_done(self, name: str) -> Item:
        item = self.find(name)
        if item is None:
            raise KeyError(f"no item called {name!r}")
        item.done = True
        return item

    def remaining(self) -> list[Item]:
        return [item for item in self.items if not item.done]

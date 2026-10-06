import unittest

from shopping_list.model import ShoppingList


class ShoppingListTest(unittest.TestCase):
    def test_adds_new_item(self):
        shopping = ShoppingList()
        shopping.add("milk", 2)
        self.assertEqual(shopping.items[0].quantity, 2)

    def test_adding_existing_item_increases_quantity(self):
        shopping = ShoppingList()
        shopping.add("Milk")
        shopping.add("milk", 2)
        self.assertEqual(len(shopping.items), 1)
        self.assertEqual(shopping.items[0].quantity, 3)

    def test_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            ShoppingList().add("  ")

    def test_rejects_quantity_below_one(self):
        with self.assertRaises(ValueError):
            ShoppingList().add("eggs", 0)

    def test_mark_done_removes_item_from_remaining(self):
        shopping = ShoppingList()
        shopping.add("eggs")
        shopping.add("bread")
        shopping.mark_done("eggs")
        self.assertEqual([item.name for item in shopping.remaining()], ["bread"])

    def test_mark_done_raises_for_unknown_item(self):
        with self.assertRaises(KeyError):
            ShoppingList().mark_done("cheese")


if __name__ == "__main__":
    unittest.main()

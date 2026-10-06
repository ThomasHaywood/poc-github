import tempfile
import unittest
from pathlib import Path

from shopping_list import storage
from shopping_list.model import ShoppingList


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "list.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_file_loads_empty_list(self):
        self.assertEqual(storage.load(self.path).items, [])

    def test_round_trips_items(self):
        shopping = ShoppingList()
        shopping.add("milk", 2)
        shopping.add("eggs")
        shopping.mark_done("eggs")

        storage.save(shopping, self.path)

        self.assertEqual(storage.load(self.path), shopping)

    def test_save_leaves_no_temp_file_behind(self):
        storage.save(ShoppingList(), self.path)
        self.assertEqual([p.name for p in Path(self.tmp.name).iterdir()], ["list.json"])


if __name__ == "__main__":
    unittest.main()

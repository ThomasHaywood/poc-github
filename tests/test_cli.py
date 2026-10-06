import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from shopping_list.__main__ import main


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = str(Path(self.tmp.name) / "list.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--file", self.file, *args])
        return code, out.getvalue()

    def test_list_shows_only_remaining_items(self):
        self.run_cli("add", "milk", "2")
        self.run_cli("add", "eggs")
        self.run_cli("done", "eggs")

        code, output = self.run_cli("list")

        self.assertEqual(code, 0)
        self.assertEqual(output, "- milk x2\n")

    def test_done_on_unknown_item_fails(self):
        code, _ = self.run_cli("done", "cheese")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()

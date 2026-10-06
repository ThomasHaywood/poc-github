import argparse
import sys
from pathlib import Path

from shopping_list import storage

DEFAULT_PATH = Path("shopping-list.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shopping_list")
    parser.add_argument("--file", type=Path, default=DEFAULT_PATH)
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add an item")
    add.add_argument("name")
    add.add_argument("quantity", type=int, nargs="?", default=1)

    done = commands.add_parser("done", help="tick off an item")
    done.add_argument("name")

    commands.add_parser("list", help="show remaining items")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    shopping = storage.load(args.file)

    try:
        if args.command == "add":
            item = shopping.add(args.name, args.quantity)
            print(f"{item.name} x{item.quantity}")
        elif args.command == "done":
            shopping.mark_done(args.name)
        elif args.command == "list":
            for item in shopping.remaining():
                print(f"- {item.name} x{item.quantity}")
    except (ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    storage.save(shopping, args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())

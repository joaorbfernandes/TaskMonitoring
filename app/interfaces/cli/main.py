import argparse
from app.interfaces.cli.commands.create_task import (
    register_create_task_command,
)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_create_task_command(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
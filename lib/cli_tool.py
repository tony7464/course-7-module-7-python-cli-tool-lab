import argparse

try:
    from lib.models import Task, User
except ImportError:
    from models import Task, User

# Session store: user name -> User. Each User holds a list of Task objects.
users = {}

# Seeded so complete-task can be tested without file persistence
alice = User("Alice")
unit_test_task = Task("Write unit tests")
alice.add_task(unit_test_task)
users["Alice"] = alice


def non_empty(value):
    """argparse type: reject blank strings before a command runs."""
    if not value or not str(value).strip():
        raise argparse.ArgumentTypeError("value cannot be empty")
    return str(value).strip()


def get_or_create_user(name):
    user = users.get(name) or User(name)
    users[name] = user
    return user


def add_task(args):
    user = get_or_create_user(args.user)
    user.add_task(Task(args.title))


def complete_task(args):
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return
    user.complete_task(args.title)


def list_tasks(args):
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return
    user.list_tasks()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Task Manager CLI",
        epilog="Example: python -m lib.cli_tool add-task Alice \"Write unit tests\"",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available commands",
    )

    add_parser = subparsers.add_parser("add-task", help="Add a new task for a user")
    add_parser.add_argument("user", type=non_empty, help="Name of the user who owns the task")
    add_parser.add_argument("title", type=non_empty, help="Title of the task to add")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Mark a user's task as complete")
    complete_parser.add_argument("user", type=non_empty, help="Name of the user who owns the task")
    complete_parser.add_argument("title", type=non_empty, help="Title of the task to complete")
    complete_parser.set_defaults(func=complete_task)

    list_parser = subparsers.add_parser("list-tasks", help="List all tasks for a user")
    list_parser.add_argument("user", type=non_empty, help="Name of the user whose tasks to list")
    list_parser.set_defaults(func=list_tasks)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

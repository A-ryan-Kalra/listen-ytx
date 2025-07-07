import re
import typer, os
from os.path import expanduser
import json
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import print
import shutil
from rich.markdown import Markdown
from datetime import datetime
from functools import wraps

app = typer.Typer()
console = Console()

STYLE_SUCCESS = "bold green on #FFFDD0"
STYLE_WARNING = "bold magenta on grey11"
STYLE_NORMAL = "green on black"


def write_config(data: dict) -> None:
    with open(config_file_path, "w") as w_file:
        json.dump(data, w_file, indent=2)


def is_valid_index(index):
    return 0 <= index < len(config["tasks"])


def center_print(text, wrap: bool = False, style=None, justify=None):

    if wrap:
        width = shutil.get_terminal_size().columns // 2
    else:
        width = shutil.get_terminal_size().columns

    console.print(
        Align.center(
            text,
            style=style,
            width=width,
        ),
        style=style,
        justify=justify,
    )
    print()


def read_config() -> None:
    global config
    with open(config_file_path) as r_file:
        config = json.load(r_file)


def greet_user(func):
    """
    Decorator that prints a personalized greeting banner before executing any function.
    """

    @wraps(func)
    def show_message(*args, **kwargs):
        now = datetime.now()
        try:
            username = re.split(r"[ _-]", config["username"])[0]
            formatted = now.strftime(config["timezone"])
        except:
            username = "User"
            formatted = now.strftime("%d-%B-%Y | %H:%M %Z")

        os.system("cls" if os.name == "nt" else "clear")
        console.rule(
            f"[yellow bold] Hey [magenta bold]{username}![/] It's [yellow bold]{formatted}[/][/] ",
            style="yellow bold",
            align="center",
        )
        print()
        return func(*args, **kwargs)

    return show_message


@app.command(short_help="Show all the tasks.")
def lists() -> None:
    all_tasks = config["tasks"]
    table = Table(
        title="Tasks",
        header_style="#c6c8bc",
        title_style="#7c7b7b bold",
        border_style="#ae4fdd",
        padding=(0, 1),
    )

    table.add_column(
        "No.",
        style="bold #a3a8a7",
        justify="center",
    )
    table.add_column(
        "Tasks",
        style="#35d6d6",
        #  min_width=50,
        justify="left",
    )
    table.add_column(
        "Status",
        style="magenta",
        justify="center",
    )

    if len(all_tasks) == 0:
        center_print(table)
        center_print(
            "\n[#40c132]Good job, your list is empty... 😄[/]\n[cyan bold]Try adding more to your list.📝[/]",
            wrap=True,
            justify="center",
        )
        return

    for index, task in enumerate(all_tasks, 1):
        if task["status"] == "pending":
            task_no = f"[red]{index}[/]"
            task_name = f"[red bold]{task["name"]}[/]"
            task_status = f"[red]❌[/]"
            table.add_row(task_no, task_name, task_status)
        else:
            task_no = f"[green]{index}[/]"
            task_name = f"[green bold]{task["name"]}[/]"
            task_status = f"[green]✅[/]"
            table.add_row(task_no, task_name, task_status)

    center_print(table)


@app.command(short_help="Swap the position of the tasks.")
@greet_user
def swap(old_index: int, new_index: int) -> None:

    old_index, new_index = old_index - 1, new_index - 1

    if len(config["tasks"]) == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )
        return

    elif is_valid_index(old_index) and is_valid_index(new_index):
        if old_index == new_index:
            center_print(
                "\nThe task is already at that position. Nothing to move!",
                style=STYLE_WARNING,
            )
            return
        else:
            config["tasks"][old_index], config["tasks"][new_index] = (
                config["tasks"][new_index],
                config["tasks"][old_index],
            )
            write_config(config)
            center_print("Task Updated!", style=STYLE_SUCCESS, wrap=True)

            lists()
    else:
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_WARNING,
        )


@app.command(short_help="Move a task to a specific position in the table.")
@greet_user
def move(old_index: int, new_index: int) -> None:

    old_index, new_index = old_index - 1, new_index - 1

    if len(config["tasks"]) == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )
        return

    elif is_valid_index(old_index) and is_valid_index(new_index):
        if old_index == new_index:
            center_print(
                "\nThe task is already at that position. Nothing to move!",
                style=STYLE_WARNING,
            )
            return
        else:
            move_task = config["tasks"].pop(old_index)
            config["tasks"].insert(new_index, move_task)
            write_config(config)
            center_print("Task Updated!", style=STYLE_SUCCESS, wrap=True)

            lists()
    else:
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_WARNING,
        )


@app.command(short_help="Complete a task by its number.")
@greet_user
def do(index: int) -> None:

    index = index - 1
    if len(config["tasks"]) == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )
        return

    if is_valid_index(index):
        if config["tasks"][index]["status"] == "completed":
            center_print("Task is already completed!", style=STYLE_SUCCESS, wrap=True)
            lists()

        else:
            config["tasks"][index]["status"] = "completed"
            write_config(config)
            center_print("Task Updated!", style=STYLE_SUCCESS, wrap=True)
            lists()
    else:
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_WARNING,
        )


@app.command(short_help="Undo a task by its number.")
@greet_user
def undo(index: int) -> None:

    index = index - 1
    if config["tasks"] == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )
        return
    elif is_valid_index(index):
        if config["tasks"][index]["status"] == "pending":
            center_print("The task is already pending.", style=STYLE_SUCCESS, wrap=True)
            lists()
        else:
            config["tasks"][index]["status"] = "pending"
            write_config(config)
            center_print("Task Updated!", style=STYLE_SUCCESS, wrap=True)
            lists()

    else:
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_WARNING,
        )


@app.command(short_help="Add a new task.")
@greet_user
def add(data: str) -> None:
    #
    center_print(
        f"[green bold]'{data}'[/] [blue]added to the list![/]",
        wrap=True,
    )
    task = {"name": data, "status": "pending"}
    config["tasks"].append(task)
    write_config(config)
    lists()


@app.command(short_help="Delete a task.")
@greet_user
def remove(index: int) -> None:

    index = index - 1

    if len(config["tasks"]) == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )

    elif not is_valid_index(index):
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_WARNING,
        )
    else:
        center_print(
            f"[blue]Deleted[/] [red]'{config["tasks"][index]['name']}'[/]",
        )
        del config["tasks"][index]
        write_config(config)
        lists()


@app.command(short_help="Edit a specific task in the list.")
@greet_user
def edit(index: int, text: str) -> None:

    index = index - 1
    if not text.strip():
        center_print(
            "Text is missing",
            style=STYLE_WARNING,
        )
        return

    if len(config["tasks"]) == 0:
        center_print(
            "Oops, the list is empty.\nUse [green]'add'[/] to add a new task to the lists. 📝",
            style=STYLE_WARNING,
            justify="center",
        )
        return
    if not is_valid_index(index):
        center_print(
            f"Please select a valid number between (1 - {len(config["tasks"])})",
            style=STYLE_SUCCESS,
        )
    else:
        config["tasks"][index]["name"] = text
        write_config(config)
        center_print("Task Updated!", style=STYLE_SUCCESS, wrap=True)
        lists()


@app.command(short_help="Change Your Name")
@greet_user
def callme(name: str) -> None:

    config["username"] = name
    write_config(config)
    center_print(
        f"\nSure! Going forward, I will address you as {name} 🦄\n",
        style="magenta bold",
    )


@app.command(short_help="Clear all the tasks")
@greet_user
def clearall():

    if len(config["tasks"]) != 0:
        config["tasks"].clear()
        center_print("🧹💨 Cleared all tasks.", style=STYLE_WARNING)
        write_config(config)
        lists()

    else:
        lists()


@app.command(short_help="Reset all and initialize new setup.")
def setup_file():

    config = {}
    config["tasks"] = []
    center_print(
        "Welcome to listen-ytx\n[magenta]Your only task manager![/] 📝",
        style="bold #FFFDD0 on grey11",
        justify="center",
    )
    config["username"] = input(
        "\nHey there! 👋😁\nBefore we proceed, let's start with your name. What should I call you?\n> "
    )
    console.print("\nThank you for letting me know your name!", style="yellow bold")

    while True:
        choice = input(
            "\nWhich time format would you like to use (1/2)?\n[1] 12-hour (e.g., 02:30 PM)\n[2] 24-hour (e.g., 14:30)\n> "
        )
        if choice == "1":
            formatted = "%d-%B-%Y | %I:%M %p"

            break
        elif choice == "2":
            formatted = "%d-%B-%Y | %H:%M %Z"
            break
        else:
            console.print("\nInvalid choice\n")

    console.print("\nThat's great!\n", style="yellow")

    config["timezone"] = formatted
    config["init_setup_done"] = True

    write_config(config)

    console.print(
        "> If you wish to change your name later, you can type:",
        style="bold white",
    )
    console.print(
        '> [bold green]listen callme "Your-Name" [/bold green]',
    )

    console.print(
        "\nPlease type [cyan bold]'listen'[/] to fetch your list.\n", style=""
    )


@app.callback(invoke_without_command=True)
@greet_user
def initialize(ctx: typer.Context):

    if ctx.invoked_subcommand is None:
        lists()


def main():
    # global config_path

    config_path = os.path.join(expanduser("~"), ".config", "listen-ytx")
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    global config_file_path
    config_file_path = os.path.join(config_path, "config.json")
    try:
        with open(config_file_path) as config_file:
            global config
            config = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        typer.run(setup_file)

    else:
        if "init_setup_done" in config and config["init_setup_done"] is True:
            app()
        else:
            typer.run(setup_file)


main()

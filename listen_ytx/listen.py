import typer, os
from os.path import expanduser
import json

app = typer.Typer()


def write_config(data: dict) -> None:
    with open(config_file_path, "w") as w_file:
        json.dump(data, w_file, indent=2)


def read_config() -> None:
    global config
    with open(config_file_path) as r_file:
        config = json.load(r_file)


@app.command(short_help="Add a new task.")
def add(data: str) -> None:
    task = {"name": data, "status": "pending"}
    config["tasks"].append(task)
    write_config(config)


@app.command(short_help="Show all the tasks.")
def show() -> None:
    for index, task in enumerate(config["tasks"], 1):
        print(f"{index}. {task}\n")


@app.command(short_help="Complete a task by its number.")
def do(index: int) -> None:
    index = index - 1
    if len(config["tasks"]) == 0:
        print("\nOops, list is empty.\n")
        return

    if 0 <= index < len(config["tasks"]):
        if config["tasks"][index]["status"] == "completed":
            print("\nTask is already done!\n")
        else:
            config["tasks"][index]["status"] = "completed"
            write_config(config)
            print("\nTask completed successfully!\n")
    else:
        print(f"Please select a valid number between (1 - {len(config["tasks"])})")


@app.command(short_help="Undo a task by its number.")
def undo(index: int) -> None:
    index = index - 1
    if config["tasks"] == 0:
        print("\nOops, list is empty.\n")
        return
    elif 0 <= index < len(config["tasks"]):
        if config["tasks"][index]["status"] == "pending":
            print("\nThe task is already pending.\n")
        else:
            config["tasks"][index]["status"] = "pending"
            write_config(config)
            print("\nTask undone successfully!\n")

    else:
        print(f"Please select a valid number between (1 - {len(config["tasks"])})")


@app.command(short_help="Delete a task.")
def remove(index: int) -> None:
    index = index - 1

    if len(config["tasks"]) == 0:
        print("\nOops, the list is empty.")

    elif not 0 <= index < len(config["tasks"]):
        print(f"Please select a valid number between (1 - {len(config["tasks"])})")
    else:
        del config["tasks"][index]
        write_config(config)
        print("\nTask deleted successfully!\n")


@app.command(short_help="Reset all and initialize new setup.")
def setup_file():

    config = {}
    config["tasks"] = []
    config["init_setup_done"] = True

    write_config(config)
    # __location__ = os.path.dirname(os.path.realpath(__file__))

    # config["location"] = __location__
    # print(__location__)


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

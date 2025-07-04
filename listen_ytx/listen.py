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


@app.command()
def add(task: str) -> None:
    config["tasks"].append(task)
    write_config(config)
    print(config["tasks"])


@app.command()
def show() -> None:
    for index, task in enumerate(config["tasks"], 1):
        print(f"\n{index}. {task}")


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

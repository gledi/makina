from pathlib import Path

from environs import Env


def file_contents(filename: str | Path) -> str:
    path = filename if isinstance(filename, Path) else Path(filename)
    with path.open("r") as file:
        contents = file.read()
    return contents.strip()


def setup_env(env: Env) -> None:
    env.add_parser("filecontents", file_contents)

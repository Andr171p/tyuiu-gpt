from typing import Union

from pathlib import Path


def load_txt(file_path: Union[Path, str]) -> str:
    with open(
        file=file_path,
        mode="r",
        encoding="utf-8",
    ) as file:
        return file.read()

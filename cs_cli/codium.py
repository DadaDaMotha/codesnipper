import typing as t
from pathlib import Path

from cs_cli.types import StringOrPath

codium_config_base = Path("~/.config/VSCodium/User").expanduser()


vscode_config_base = Path("~/.config/VSCode/User").expanduser()


def config_dir(
    on_fail: t.Callable[[StringOrPath], None],
):
    config_base = None
    for maybe_dir in (codium_config_base, vscode_config_base):
        if maybe_dir.is_dir():
            config_base = maybe_dir

    if not config_base:
        on_fail(f"vscodium/vscode not installed using apt/snap.")
        return
    return config_base

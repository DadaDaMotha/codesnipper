import contextlib
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import pytest
from typer.testing import CliRunner

from cs_cli.constants import SNIPPETS_ROOT_ENV

fixture_path = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="function")
def temporary_directory():
    """Provides a temporary directory that is removed after the test."""
    directory = tempfile.mkdtemp()
    yield Path(directory)
    shutil.rmtree(directory)


@contextlib.contextmanager
def cd_to_directory(path: Path, env: Optional[dict] = None):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    if env:
        for k, v in env.items():
            os.environ[k] = v
    try:
        yield
    finally:
        os.chdir(prev_cwd)
        if env:
            for k in env:
                os.environ[k] = ""


@pytest.fixture()
def runner(temporary_directory):
    assert fixture_path.is_dir(), "Run tests from git root directory"
    with cd_to_directory(
        temporary_directory, env={SNIPPETS_ROOT_ENV: str(fixture_path)}
    ):
        yield CliRunner()

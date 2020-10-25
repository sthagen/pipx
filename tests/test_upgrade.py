import pytest  # type: ignore

from helpers import mock_legacy_venv, run_pipx_cli


def test_upgrade(pipx_temp_env, capsys):
    assert run_pipx_cli(["upgrade", "pycowsay"])
    assert not run_pipx_cli(["install", "pycowsay"])
    assert not run_pipx_cli(["upgrade", "pycowsay"])


@pytest.mark.parametrize("metadata_version", [None, "0.1"])
def test_upgrade_legacy_venv(pipx_temp_env, capsys, metadata_version):
    assert run_pipx_cli(["upgrade", "pycowsay"])
    assert not run_pipx_cli(["install", "pycowsay"])
    mock_legacy_venv("pycowsay", metadata_version=metadata_version)
    assert not run_pipx_cli(["upgrade", "pycowsay"])


def test_upgrade_suffix(pipx_temp_env, capsys):
    name = "pycowsay"
    suffix = "_a"

    assert not run_pipx_cli(["install", name, f"--suffix={suffix}"])
    assert run_pipx_cli(["upgrade", f"{name}"])
    assert not run_pipx_cli(["upgrade", f"{name}{suffix}"])


@pytest.mark.parametrize("metadata_version", ["0.1"])
def test_upgrade_suffix_legacy_venv(pipx_temp_env, capsys, metadata_version):
    name = "pycowsay"
    suffix = "_a"

    assert not run_pipx_cli(["install", name, f"--suffix={suffix}"])
    mock_legacy_venv(f"{name}{suffix}", metadata_version=metadata_version)
    assert run_pipx_cli(["upgrade", f"{name}"])
    assert not run_pipx_cli(["upgrade", f"{name}{suffix}"])


def test_upgrade_specifier(pipx_temp_env, capsys):
    name = "pylint"
    specifier = "==2.3.1"
    initial_version = "2.3.1"

    assert not run_pipx_cli(["install", f"{name}{specifier}"])
    assert run_pipx_cli(["upgrade", f"{name}"])
    captured = capsys.readouterr()
    assert f"upgraded package {name} from {initial_version} to" in captured.out

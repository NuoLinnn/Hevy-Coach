import pytest

from hevy_coach import __version__
from hevy_coach.cli import build_parser, main


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_plan_defaults() -> None:
    args = build_parser().parse_args(["plan", "--routine", "Push A"])
    assert args.routine == "Push A"
    assert args.apply is False
    assert str(args.config) == "hevy-coach.toml"


def test_plan_requires_routine() -> None:
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["plan"])
    assert exc.value.code == 2

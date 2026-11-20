"""Command-line entry point: hevy-coach plan --routine NAME [--apply] (SPEC §2)."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from hevy_coach import __version__

EXIT_OK = 0
EXIT_CONFIG = 1
EXIT_API = 2
EXIT_NOT_FOUND = 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hevy-coach",
        description="Plan the next weights and reps for a Hevy routine.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="plan the next session of a routine")
    plan.add_argument("--routine", required=True, help="Hevy routine title")
    plan.add_argument(
        "--config",
        type=Path,
        default=Path("hevy-coach.toml"),
        help="configuration file (default: ./hevy-coach.toml)",
    )
    plan.add_argument(
        "--apply", action="store_true", help="update the routine in Hevy"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "plan":
        print("hevy-coach: error: plan is not implemented yet", file=sys.stderr)
        return EXIT_CONFIG
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """epyfun."""


if __name__ == "__main__":
    main(prog_name="epyfun")  # pragma: no cover

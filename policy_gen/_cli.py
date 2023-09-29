from pathlib import Path
from typing import List

import click

from .generator import create_pdf


@click.command()
@click.argument("input_files", nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--output-folder", "-o", default=".", type=click.Path(exists=True, file_okay=False)
)
def generate(input_files: List[str], output_folder: str):
    if not input_files:
        raise click.UsageError("You must provide at least one input file.")

    output_folder = Path(output_folder)
    for input_file in input_files:
        input_file = Path(input_file)
        output_file = output_folder / input_file.with_suffix(".pdf").name
        create_pdf(input_file, output_file)
        click.echo(f"Generated {output_file}")

from typing import Annotated
import typer

from loremaster import config, scriptorium

app = typer.Typer(rich_markup_mode="markdown", context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def main(
    concept: Annotated[
        str, typer.Argument(help="Concept for the character to describe.")
    ],
    text_style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            help="Style to be used for textual output.",
        ),
    ] = config.DEFAULT_TEXT_STYLE,
    visual_style: Annotated[
        str,
        typer.Option(
            "--visual",
            "-v",
            help="Style to be used for the generated image.",
        ),
    ] = config.DEFAULT_VISUAL_STYLE,
    paragraphs: Annotated[
        int,
        typer.Option(
            "--paragraphs",
            "-p",
            help="Number of paragraphs in the literary description.",
        ),
    ] = config.DEFAULT_PARAGRAPHS,
):
    inputs = {
        "concept": concept,
        "text_style": text_style,
        "visual_style": visual_style,
        "paragraphs": paragraphs,
    }

    flow = scriptorium.LoreMasterFlow()
    flow_output = flow.kickoff(inputs=inputs)

    for name, output in flow_output.items():
        print("###", name.title(), "###\n")
        print(f"{output}\n\n")


if __name__ == "__main__":
    app()

from typing import Annotated

import typer

from loremaster import scriptorium
from loremaster.config import settings

app = typer.Typer(
    rich_markup_mode="markdown",
    context_settings={"help_option_names": ["-h", "--help"]},
)


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
    ] = settings.DEFAULT_TEXT_STYLE,
    visual_style: Annotated[
        str,
        typer.Option(
            "--visual",
            "-v",
            help="Style to be used for the generated image.",
        ),
    ] = settings.DEFAULT_VISUAL_STYLE,
    paragraphs: Annotated[
        int,
        typer.Option(
            "--paragraphs",
            "-p",
            help="Number of paragraphs in the literary description.",
        ),
    ] = settings.DEFAULT_PARAGRAPHS,
    plot: Annotated[
        bool,
        typer.Option(
            "--plot",
            help="Generate the plot of the agentic flow. Ignore all other options.",
        ),
    ] = False,
):
    inputs = {
        "concept": concept,
        "text_style": text_style,
        "visual_style": visual_style,
        "paragraphs": paragraphs,
    }

    flow = scriptorium.LoreMasterFlow()

    if plot:
        flow.plot()
    else:
        flow_output = flow.kickoff(inputs=inputs)

        print("### Description ###")
        print(flow_output.description)
        print("")

        print("### Literary Description ###")
        print(flow_output.literary_description)
        print("")

        print("### Image Prompt ###")
        print(flow_output.image_prompt)
        print("")

        print("### Generated Image ###")
        print("Generated Image")
        print(flow_output.image_url)


if __name__ == "__main__":
    app()

import streamlit as st

from loremaster import scriptorium
from loremaster.config import settings


def main():


    with st.form("inputs_form"):
        concept = st.text_area(
            label="Character Concept",
            placeholder=(
                "Enter a description of your character concept, for example:"
                " Fantasy warrior with a sword, getting ready to defend from an attack."
            )
        )
        text_style = st.text_input(
            label="Textual Style",
            value=settings.DEFAULT_TEXT_STYLE,
            placeholder="Style to be used for textual output.",
        )
        visual_style = st.text_input(
            label="Visual Style",
            value=settings.DEFAULT_VISUAL_STYLE,
            placeholder="Style to be used for the generated image.",
        )
        paragraphs = st.number_input(
            label="Number of Paragraphs",
            value=settings.DEFAULT_PARAGRAPHS,
            placeholder="Number of paragraphs in the literary description.",
        )
        submit_form = st.form_submit_button('Generate Character')


    if submit_form and concept:
        inputs = {
            "concept": concept,
            "text_style": text_style,
            "visual_style": visual_style,
            "paragraphs": paragraphs,
        }

        flow = scriptorium.LoreMasterFlow()
        flow_output: scriptorium.FlowOutputs = flow.kickoff(inputs=inputs)

        st.title("Loremaster: Characters")

        st.header("Description")
        st.markdown(flow_output.description)

        st.header("Literary Description")
        st.markdown(flow_output.literary_description)

        st.header("Image")

        st.subheader("Image Prompt")
        st.markdown(flow_output.image_prompt)

        st.subheader("Generated Image")
        st.image(str(flow_output.image_url))

    else:
        st.text("Waiting for a character concept!")


if __name__ == "__main__":
    main()

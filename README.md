# LoreMaster

LoreMaster is a small agentic AI workflow with the following functionalities:

First, the workflow takes the following details as input:
* some information about the setting
* short description of a fictional character concept
* optional: name for the character
* optional: details about the desired styles for the writing and image

If the name is not provided, the agent will generate one based on the setting. Similarly, if the style details are not provided, it will try to infer the most appropriate ones, based on the setting details.

Then, the flow generates a detailed narrative description of the character.

Finally, as an option, the flow can generate a relevant prompt and trigger the generation of an image of that character, in the corresponding setting, in the specified or inferred visual style.

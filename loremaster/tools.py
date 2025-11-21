import base64

import cloudinary.uploader
from crewai.tools import BaseTool
from google import genai

from loremaster.config import settings

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_API_KEY,
    api_secret=settings.CLOUD_API_SECRET,
    secure=True,
)

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)


class ImagenTool(BaseTool):
    """Generates images using an Imagen model."""

    name: str = "Imagen Generator"
    description: str = (
        "Generates a high-quality image from a text prompt using the Imagen model."
    )

    def _run(self, prompt: str) -> str:
        """
        Generates the image and returns a URL or a confirmation message.
        """
        # Call the Imagen model via the Gemini client
        response = gemini_client.models.generate_images(
            model=settings.IMAGEN_MODEL,
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                # You can add more configurations here, like aspect_ratio='16:9'
            ),
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes  # type: ignore [union-attr]
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            return f"data:image/png;base64,{encoded_image}"
        else:
            raise RuntimeError(  # noqa: TRY003
                "ERROR: Image generation failed to return a valid image."
            )


class GeminiImageTool(BaseTool):
    """Generates images using a Gemini model.."""

    name: str = "Gemini Image Generator"
    description: str = (
        "Generates a high-quality image from a text prompt using a Gemini model."
    )

    def _run(self, prompt: str) -> str:
        """
        Generates the image and returns a URL or a confirmation message.
        """
        response = gemini_client.models.generate_content(
            model=settings.GEMINI_IMAGE_MODEL,
            contents=f"Generate an image based on the following description: {prompt}",
            config=genai.types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_data = part.inline_data.data
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                return f"data:image/png;base64,{encoded_image}"

        raise RuntimeError(  # noqa: TRY003
            "ERROR: Image generation failed to return a valid image."
        )


image_generation = {
    "imagen": ImagenTool,
    "gemini": GeminiImageTool,
}

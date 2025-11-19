from io import BytesIO
import base64
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from crewai.tools import BaseTool
from google import genai
from uuid_extensions import uuid7

from loremaster.config import settings

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_API_KEY,
    api_secret=settings.CLOUD_API_SECRET,
    secure=True,
)

from loremaster.config import settings

# Initialize the Gemini client
# It will automatically pick up the GEMINI_API_KEY from your environment
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

settings.images_dir.mkdir(exist_ok=True)


# Define the custom tool class
class GeminiImageGeneratorTool(BaseTool):
    name: str = "Gemini Image Generator"
    description: str = (
        "Generates a high-quality image from a text prompt using the Imagen model."
    )

    def _run(self, prompt: str) -> str:
        """
        Generates the image and returns a URL or a confirmation message.
        """
        # Call the Imagen model via the Gemini client
        response = gemini_client.models.generate_images(
            model=settings.GEMINI_IMAGE_MODEL,
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                # You can add more configurations here, like aspect_ratio='16:9'
            ),
        )

        if response.generated_images:
            # The response contains the image data.
            # In a production app, you would upload this to a cloud storage (like GCS)
            # and return the public URL. For simplicity, we'll return a confirmation
            # and you can add code to save it.

            # --- Example: Save to a file (You'd need io and PIL for this) ---
            image_data = response.generated_images[0].image.image_bytes
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/png;base64,{encoded_image}"
        else:
            raise RuntimeError(
                "ERROR: Image generation failed to return a valid image."
            )

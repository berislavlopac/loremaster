from io import BytesIO

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

    def _run(self, prompt: str) -> BytesIO:
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
            image_id = uuid7()
            public_image_id = image_id.hex

            upload_result = cloudinary.uploader.upload(
                BytesIO(image_data), public_id=public_image_id
            )
            # secure_url = upload_result["secure_url"]

            # Optimize delivery by resizing and applying auto-format and auto-quality
            optimize_url, _ = cloudinary_url(
                public_image_id, fetch_format="auto", quality="auto"
            )
            return optimize_url

            # Transform the image: auto-crop to square aspect_ratio
            # auto_crop_url, _ = cloudinary_url(image_id, width=500, height=500, crop="auto", gravity="auto")
            # print(auto_crop_url)

            # return f"SUCCESS: Image generated using Imagen. You would typically retrieve the image data and save/host it now. Confirmation: {response.generated_images[0].seed}."
        else:
            raise RuntimeError(
                "ERROR: Image generation failed to return a valid image."
            )

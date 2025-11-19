from crewai.tools import BaseTool
from google import genai
from PIL import Image
from io import BytesIO
from time import time
from loremaster import config

# Initialize the Gemini client
# It will automatically pick up the GEMINI_API_KEY from your environment
gemini_client = genai.Client(api_key=config.GEMINI_API_KEY)

config.BASE_IMAGES_DIR.mkdir(exist_ok=True)


# Define the custom tool class
class GeminiImageGeneratorTool(BaseTool):
    name: str = "Gemini Image Generator"
    description: str = (
        "Generates a high-quality image from a text prompt using the Imagen model."
    )

    def _run(self, prompt: str):
        """
        Generates the image and returns a URL or a confirmation message.
        """
        # Call the Imagen model via the Gemini client
        response = gemini_client.models.generate_images(
            model= config.GEMINI_IMAGE_MODEL,
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
            image = Image.open(BytesIO(image_data))
            timestamp = int(time() * 100000)
            file_path = config.BASE_IMAGES_DIR / f"character-{timestamp}.png"
            image.save(file_path)
            return file_path

            # return f"SUCCESS: Image generated using Imagen. You would typically retrieve the image data and save/host it now. Confirmation: {response.generated_images[0].seed}."
        else:
            raise RuntimeError("ERROR: Image generation failed to return a valid image.")

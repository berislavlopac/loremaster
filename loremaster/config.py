from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

BASE_DIR: Path = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="loremaster_", env_file=".env")

    GEMINI_API_KEY: str
    CLOUD_NAME: str
    CLOUD_API_KEY: str
    CLOUD_API_SECRET: str

    GEMINI_MODEL: str = "gemini/gemini-2.5-flash"
    GEMINI_IMAGE_MODEL: str = "imagen-4.0-generate-001"
    DEFAULT_TEMPERATURE: float = 0.8
    DEBUG: bool = False

    DEFAULT_TEXT_STYLE: str = "traditional fantasy novel"
    DEFAULT_VISUAL_STYLE: str = "hand-drawn pencil sketch"
    DEFAULT_PARAGRAPHS: int = 2

    AGENTS_CONFIG_FILE: str = "agents.yaml"
    IMAGES_DIR_PATH: str = "images"

    @property
    def images_dir(self) -> Path:
        return BASE_DIR / self.IMAGES_DIR_PATH

    @property
    def agents(self):
        return yaml.safe_load((BASE_DIR / self.AGENTS_CONFIG_FILE).read_text())


settings = Settings()  # type: ignore [call-arg]

from crewai import LLM, Agent, Flow
from crewai.flow.flow import and_, listen, start
from pydantic import AnyUrl, BaseModel

from loremaster import tools
from loremaster.config import settings

image_generator = tools.image_generation[settings.IMAGE_GENERATION_TOOL]

# --- AGENTS ---
agents = {}
for name, conf in settings.agents.items():
    temperature = conf.pop("temperature", settings.DEFAULT_TEMPERATURE)
    agents[name] = Agent(
        **conf,
        verbose=settings.DEBUG,
        allow_delegation=False,
        llm=LLM(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY,
            temperature=temperature,
        ),
        max_retry_limit=settings.MAX_RETRIES,
    )


# --- FLOW ---
class FlowOutputs(BaseModel):
    description: str
    literary_description: str
    image_prompt: str
    image_url: str


class LoreMasterFlow(Flow):
    @start()
    def observe(self):
        """Convert the user input into a detailed description of the character."""
        print("--- Observing...")
        agent = agents["creative_writer"]
        query = (
            "Generate a detailed description based on this concept: '{concept}'."
            " Ensure that the description is clear and detailed,  filling in for any"
            " obviously missing elements. The output must be four or less paragraphs"
            " of clear and detailed description."
        ).format(**self.state)
        result = agent.kickoff(query)
        self.state["description"] = str(result)

    @listen(observe)
    def describe(self):
        """Convert the observed description into a literary description."""
        print("--- Describing...")
        agent = agents["literary_architect"]
        query = (
            "Take this character description and convert it into a detailed,"
            " {paragraphs}-paragraph character description: {description}."
            " Ensure the text strictly adheres to the following textual style:"
            " '{text_style}'."
            " The output MUST be the narrative description only."
        ).format(**self.state)
        result = agent.kickoff(query)
        self.state["literary_description"] = str(result)

    @listen(observe)
    def visualise(self):
        """Convert the observed description into an image generation prompt.."""
        print("--- Visualising...")
        agent = agents["prompt_engineer"]
        query = (
            "Take this description of the character and convert it into a single, highly"
            " optimized, comma-separated image generation prompt: '{description}'."
            " Crucially, ensure the prompt includes the specific visual style: '{visual_style}'."
            " Your final output MUST be the prompt string only (no extra commentary or text)."
        ).format(**self.state)
        result = agent.kickoff(query)
        self.state["image_prompt"] = str(result)

    @listen(visualise)
    def illuminate(self):
        """Generate image based on the generated prompt."""
        print("--- Illuminating...")
        image_generator = tools.image_generation[settings.IMAGE_GENERATION_TOOL]
        image_tool = image_generator()
        result = image_tool._run(self.state["image_prompt"])
        self.state["image_url"] = str(result)

    @listen(and_(describe, illuminate))
    def collect(self):
        return FlowOutputs.model_validate(self.state)

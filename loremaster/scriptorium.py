from crewai import LLM, Agent, Crew, Process, Task, Flow
from crewai.flow.flow import and_, listen, start
from loremaster import config

from loremaster.tools import GeminiImageGeneratorTool

# --- TOOLS ---
# The image generator tool will be used by the ArtDirector Agent
available_tools = {
    "image_generator": GeminiImageGeneratorTool
}

# --- AGENTS ---
agents = {}
for name, conf in config.agents.items():
    temperature = conf.pop("temperature", config.DEFAULT_TEMPERATURE)
    tools = [available_tools[tool]() for tool in conf.pop("tools", [])]
    agents[name] = Agent(
        **conf,
        verbose=config.DEBUG,
        allow_delegation=False,
        llm=LLM(
            model=config.GEMINI_MODEL,
            api_key=config.GEMINI_API_KEY,
            temperature=temperature,
        ),
        tools=tools,
    )


# --- FLOW ---

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
        self.state["description"] = result

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
        self.state["literary_description"] = result

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
        self.state["image_prompt"] = result

    @listen(visualise)
    def illuminate(self):
        """Generate image based on the generated prompt."""
        print("--- Illuminating...")
        agent = agents["art_director"]
        query = (
            "Use the provided optimized image prompt to call the image generation tool and generate the final image."
            " Image prompt:\n\n{image_prompt}"
        ).format(**self.state)
        result = agent.kickoff(query)
        self.state["image"] = result


    @listen(and_(describe, illuminate))
    def collect(self):
        return {
            "description": self.state["description"],
            "literary_description": self.state["literary_description"],
            "image": self.state["image"],
        }

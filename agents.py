import os
from utils import load_yaml_file
from dotenv import load_dotenv, find_dotenv
from mistralai import Mistral

config_data = load_yaml_file("config.yaml")
load_dotenv(find_dotenv())

# Get API key
mistral_api_key = os.getenv("MISTRALAI_API_KEY")
client = Mistral(mistral_api_key)

def get_websearch_agent():
    """
    Create and return a web search agent using Mistral API.
    """
    websearch_agent = client.beta.agents.create(
        model=config_data["model_name"],
        description="Agent able to search information over the web",
        name="Websearch Agent",
        instructions="You have the ability to perform web searches with `web_search` to find up-to-date information. **Always provide the source URLs when you use web search to answer a question.**",
        tools=[{"type": "web_search"}],
        completion_args={
            "temperature": 0.3,
            "top_p": 0.95,
        }
    )
    return websearch_agent
from typing import List, Dict, Any
import inspect
import json
import os
from inspect import Parameter
from pydantic import create_model
from web_search import WebSearch
import yaml
from mistralai import Mistral
from dotenv import load_dotenv


load_dotenv()


# Use absolute path for config file
config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

try:
    with open(config_path, "r") as cfg_file:
        cfg = yaml.safe_load(cfg_file)
except FileNotFoundError:
    # Fallback to looking in current directory
    with open("config.yaml", "r") as cfg_file:
        cfg = yaml.safe_load(cfg_file)

# Initialize Mistral client with API key
api_key = os.environ.get("MISTRALAI_API_KEY")

if not api_key:
    raise ValueError(
        "MISTRALAI_API_KEY not found in environment variables or config file"
    )

client = Mistral(api_key=api_key)


class Apputils:

    @staticmethod
    def jsonschema(f) -> Dict:
        """
        Generate a JSON schema for the input parameters of the given function.
        Parameters:
        f (FunctionType): The function for which to generate the JSON schema.
        Returns:
        Dict: A dictionary containing the function name, description, and parameters schema.
        """
        # Build kwargs for pydantic.create_model. If a parameter has no
        # annotation, fall back to Any so create_model doesn't fail.
        kw = {}
        for n, o in inspect.signature(f).parameters.items():
            ann = o.annotation if o.annotation != Parameter.empty else Any
            default = ... if o.default == Parameter.empty else o.default
            kw[n] = (ann, default)

        # Use a safe class-name for the generated model (no spaces/backticks)
        model_name = f"InputFor_{f.__name__}"
        s = create_model(model_name, **kw).model_json_schema()

        json_format = dict(
            type="function",
            function=dict(
                name=f.__name__,
                description=f.__doc__,
                parameters=s
            )
        )
        return json_format

    @staticmethod
    def wrap_functions() -> List:
        """
        Wrap several web search functions and generate JSON schemas for each.

        Returns:
            List: A list of dictionaries, each containing the function name, description, and parameters schema.
        """
        return [
            Apputils.jsonschema(WebSearch.retrieve_web_search_results),
            Apputils.jsonschema(WebSearch.web_search_text),
            Apputils.jsonschema(WebSearch.web_search_pdf),
            Apputils.jsonschema(WebSearch.web_search_image),
            Apputils.jsonschema(WebSearch.web_search_video),
            Apputils.jsonschema(WebSearch.web_search_news),
            Apputils.jsonschema(WebSearch.web_search_map),
        ]

    @staticmethod
    def execute_json_function(response) -> List:
        """
        Execute a function based on the response from an API call.

        Parameters:
            response: The response object from the API call.

        Returns:
            List: The result of the executed function.
        """
        # Extract function name and arguments from the response
        func_name: str = response.choices[0].message.tool_calls[0].function.name
        func_args: Dict = json.loads(
            response.choices[0].message.tool_calls[0].function.arguments
        )
        # Call the function with the given arguments
        if func_name == 'retrieve_web_search_results':
            result = WebSearch.retrieve_web_search_results(**func_args)
        elif func_name == 'web_search_text':
            result = WebSearch.web_search_text(**func_args)
        elif func_name == 'web_search_pdf':
            result = WebSearch.web_search_pdf(**func_args)
        elif func_name == 'web_search_image':
            result = WebSearch.web_search_image(**func_args)
        elif func_name == 'web_search_video':
            result = WebSearch.web_search_video(**func_args)
        elif func_name == 'web_search_news':
            result = WebSearch.web_search_news(**func_args)
        elif func_name == 'web_search_map':
            result = WebSearch.web_search_map(**func_args)
        else:
            raise ValueError(f"Function '{func_name}' not found.")
        return result

    @staticmethod
    def ask_llm_function_caller(gpt_model: str, temperature: float, messages: List, function_json_list: List):
        """
        Generate a response from an OpenAI ChatCompletion API call with specific function calls.

        Parameters:
            gpt_model (str): The name of the GPT model to use.
            temperature (float): The temperature parameter for the API call.
            messages (List): List of message objects for the conversation.
            function_json_list (List): List of function JSON schemas.

        Returns:
            The response object from the OpenAI ChatCompletion API call.
        """
        response = client.chat.complete(
            model = gpt_model,
            messages = messages,
            tools = function_json_list,
            tool_choice = "any",
            parallel_tool_calls = False,
            temperature=temperature
        )
        return response

    @staticmethod
    def ask_llm_chatbot(gpt_model: str, temperature: float, messages: List):
        """
        Generate a response from an Mistral ChatCompletion API call without specific function calls.

        Parameters:
            gpt_model (str): The name of the GPT model to use.
            temperature (float): The temperature parameter for the API call.
            messages (List): List of message objects for the conversation.

        Returns:
            The response object from the Mistral ChatCompletion API call.
        """
        response = client.chat.complete(
            model = gpt_model, 
            messages = messages,
            temperature=temperature
        )
        return response
    
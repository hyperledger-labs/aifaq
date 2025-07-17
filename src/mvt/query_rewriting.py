import os
from utils import load_yaml_file_with_db_prompts, get_prompt_from_file
from dotenv import load_dotenv, find_dotenv
from langchain_mistralai.chat_models import ChatMistralAI

def query_rewriting_llm(user_query, context="Founder Institute Keystone Chapter"):
    """
    Riscrive una query utente in modo più specifico, utilizzando un LLM.
    
    Parameters:
    - user_query: La query originale dell'utente.
    - context: Il contesto su cui la query dovrebbe essere focalizzata.
    
    Returns:
    - La query riscritta in modo più specifico.
    """

    # Read config data with database prompt overrides
    config_data = load_yaml_file_with_db_prompts("config.yaml")
    load_dotenv(find_dotenv())

    # Get API keys
    mistral_api_key = os.getenv("MISTRALAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Select embeddings and LLM based on provider
    if config_data["llm_provider"] == "mistral":
        model = ChatMistralAI(
            mistral_api_key=mistral_api_key,
            model=config_data["model_name"]
        )
    else:  # default to OpenAI
        import openai
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(
            openai_api_key=openai_api_key,
            model=config_data["model_name"],
            temperature=0.7
        )

    # Read query rewriting prompt from config
    query_rewriting_prompt = get_prompt_from_file(config_data["query_rewriting_prompt"])

    messages = [
        ("system", query_rewriting_prompt),
        ("human", user_query),
    ]

    response = model.invoke(messages)
    return response.content

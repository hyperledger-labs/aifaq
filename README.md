# Hyperledger Labs AIFAQ prototype

The scope of this Hyperledger Labs project is to support the users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. We are implementing an open source conversational AI tool which replies to the questions related to specific context. This is a prototype which allows to create a chatbot running a RESTful API which requires GPU. Here the official Wiki pages: [Hyperledger Labs aifaq](https://labs.hyperledger.org/labs/aifaq.html) and [Hyperledger Labs wiki](https://wiki.hyperledger.org/display/labs/AI+FAQ). Please, read also the [Antitrust Policy and the Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). Every Monday we have a public meeting and the invitation is on the Hyperledger Labs calendar: [[Hyperledger Labs] FAQ AI Lab calls](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

## MVT branch

This branch uses streamlit as UI tool.

## Installation

Install dependencies:

```console
pip install -r requirements.txt
```

## Configuration

### Authentication Setup
This application uses Auth0 for authentication. You need to configure your Auth0 credentials:

1. Update file at `src/mvt/.streamlit/secrets.toml` with your Auth0 credentials:
```
[auth.auth0]
client_id = "your_client_id"
client_secret = "your_client_secret"
domain = "your-domain.auth0.com"
redirect_uri = "http://localhost:8501/callback"
```

You can find these credentials in your Auth0 dashboard at auth0.com after creating an application.

### API Keys
1. Rename the `.env.example` file in the `mvt` folder to `.env` and update it with your own credentials:
```
MISTRALAI_API_KEY =your_mistral_ai_api_key
```

2. (Optional) If you want to use Hugging Face API, add this to your `.env` file:
```
HF_TOKEN =your_huggingface_api_key
```

## Test

```console
streamlit run app.py
```
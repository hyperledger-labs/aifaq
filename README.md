# Hyperledger Labs AIFAQ prototype

The scope of this Hyperledger Labs project is to support the users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. We are implementing an open source conversational AI tool which replies to the questions related to specific context. This is a prototype which allows to create a chatbot running a RESTful API which requires GPU. Here the official Wiki pages: [Hyperledger Labs aifaq](https://labs.hyperledger.org/labs/aifaq.html) and [Hyperledger Labs wiki](https://wiki.hyperledger.org/display/labs/AI+FAQ). Please, read also the [Antitrust Policy and the Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). Every Monday we have a public meeting and the invitation is on the Hyperledger Labs calendar: [[Hyperledger Labs] FAQ AI Lab calls](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

## MVT branch

This branch contains a lightweight version.

### Backend MVT installation

Execute:

```console
pip install -r requirements.txt
```

to install the dependencies

then create a **.env** ([MistralAI optaining the API key](https://console.mistral.ai/api-keys/)) file in the same directory that contains open ai key and add a row like this MISTRALAI_API_KEY = "mistralai_key"

unzip file into rtdocs folder: it contains .html files.

then run:

```console
python ingest.py
```

it takes some minutes and create a new folder named faiss_index containing the knowledge base (vector database).

Now, we can start the local API running:

```console
python api.py
```

### Frontend MVT installation

In **client** folder create an **.env** that contains the API url:
NEXT_PUBLIC_API_URL=127.0.0.1:8080

Then run:

```console
npm install
```

and then run:

```console
npm run del
```

Now, open the web browser to http://localhost:3000 and type the question.

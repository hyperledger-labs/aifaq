# Hyperledger Labs AIFAQ prototype

The scope of this Hyperledger Labs project is to support the users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. We are implementing an open source conversational AI tool which replies to the questions related to specific context. This is a prototype which allows to create a chatbot running a RESTful API which requires GPU. Here the official Wiki pages: [Hyperledger Labs aifaq](https://labs.hyperledger.org/labs/aifaq.html) and [Hyperledger Labs wiki](https://wiki.hyperledger.org/display/labs/AI+FAQ). Please, read also the [Antitrust Policy and the Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). Every Monday we have a public meeting and the invitation is on the Hyperledger Labs calendar: [[Hyperledger Labs] FAQ AI Lab calls](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

## MVT branch

This branch uses streamlit as UI tool.

## Installation

Install dependencies:

```console
pip install -r requirements.txt
```

## Test

```console
streamlit run app.py
```

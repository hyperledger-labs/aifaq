# Hyperledger QA PoC

This is a Proof-of-Concept application that allows you to ask questions to a python script chatbot, fine-tuned with Hyperledger Standard Documents.
I implemented this first version, as mentee, during the Hyperledger Mentorship Program 2023.

## Use case

This NLP application allows people to access to the Hyperledger Standard Documentation.
The scope of the lab is to support the Hyperledger users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. Large Language Models have yielded remarkable results, either pay and open source tools. Today we can implement a conversational AI tool which replies to questions related to specific context.

## Architecture

The model is XML-R pre-trained ([HuggingFace deepset/xlm-roberta-large-squad2](https://huggingface.co/deepset/xlm-roberta-large-squad2)) with SQuAD Dataset. Below the architecture of the model:\
![alt text](./images/xlm_r_architecture.drawio.png)

## Pipeline

In this PoC I use Haystack ([Haystack by Deepset](https://haystack.deepset.ai/)) to Build the QA pipeline.
Below an image of the architecture:\
![alt text](./images/architecture_modern_qa.drawio.png)

I use Elastic Search as Retriever component.

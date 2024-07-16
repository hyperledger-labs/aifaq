# DEV Branch: Hyperledger Labs AIFAQ prototype

The scope of this Hyperledger Labs project is to support the users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. We are implementing an open source conversational AI tool which replies to the questions related to specific context. This is a prototype which allows to create a chatbot running a RESTful API which requires GPU. Here the official Wiki pages: [Hyperledger Labs aifaq](https://labs.hyperledger.org/labs/aifaq.html) and [Hyperledger Labs wiki](https://wiki.hyperledger.org/display/labs/AI+FAQ). Please, read also the [Antitrust Policy and the Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). Every Monday we have a public meeting and the invitation is on the Hyperledger Labs calendar: [[Hyperledger Labs] FAQ AI Lab calls](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

## Background

The system is an open source python project which implements an AI chatbot that replies to HTTP requests. The idea is to implement an open source framework/template, as example, for other communities/organizations/companies. Last results in open LLMs allow to have good performance using common HW resources.\
Below the application architecture:

<img src="./images/prototype_schema_v1.drawio.png" alt="LLM chatbot schema" width="750"/>

We use RAG (Retrieval Augmented Generation [arxiv.org](https://arxiv.org/abs/2312.10997)) for question answering use case. That technique aims to improve LLM answers by incorporating knowledge from external database (e.g. vector database).

The image depicts two workflow:

1. The data ingestion workflow
2. The chat workflow

During the ingestion phase, the system loads context documents and creates a vector database. For example, the document sources can be:

- An online software guide (readthedocs template)
- The GitHub issues and pull requests

In our case, they are the readthedocs guide and a wiki page.\
After the first phase, the system is ready to reply to user questions.

Currently, we use the open source [HuggingFace Zephyr-7b-beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta), and in the future we want to investigate other open source models.\
The user can query the system using HTTP requests, but we want to supply UI samples, as external module.

## Open Source Version

The software is under Apache 2.0 License (please check **LICENSE** and **NOTICE** files included). We use some 3rd party libraries: here is the [ASF 3rd Party License Policy](https://www.apache.org/legal/resolved.html) and here is the information for ([Assembling LICENSE and NOTICE files](https://infra.apache.org/licensing-howto.html#mod-notice)).

## Installation

<u>**This document does not contain commercial advertisement: all the tools/products/books/materials are generic and you have to consider those as examples!**</u>\
This software needs GPU for the execution: if you do not have a local GPU you could use a Cloud GPU. There are several solutions to use Cloud GPU:

1. Cloud Provider (AWS, GCP, ...)
2. On-Demand GPU Cloud (vast.ai, RunPod, ...)
3. Cloud GPU IDE

Currently, I use a Cloud GPU IDE ([Lightning Studio](https://lightning.ai/studios)), after signup/login, create new Studio (project):

![New Studio Button](/images/new_studio.png)

select the left solution:

![Select Studio Code](/images/studio_code.png)

click on the **Start** button, and rename the new Studio:

![Rename Studio](/images/rename_studio.png)

Then, and copy-paste the github api repo code:

![Copy Paste Code](/images/copy_paste_code.png)

and create two folders:

1. chromadb (it will contains vector database files)
2. rtdocs (it will contains the ReadTheDocs documentation)

That version works with Hyperledger fabric documents (Wiki and ReadTheDocs).

## Usage

### Download ReadTheDocs documentation

Open a new terminal:

![Open Terminal](/images/open_terminal.png)

and download the documentation executing the command below:

```console
wget -r -A.html -P rtdocs https://hyperledger-fabric.readthedocs.io/en/release-2.5/

```

actually, after a minute we can interrupt (CTRL + C) because it starts to download previous versions:

![Wget Command](/images/wget_rtdocs.png)

Now, we can move into rtdocs folder and move the **release-2.5** content to **rtdocs**. We need to compress the content of the folder, moving there and use that command:

![Compress files](/images/compress_files.png)

and move the readthedocs.tar.gz to the parent directory (../):

```console
- mv readthedocs.tar.gz ..
- cd ..
```

repeating the two commands until we are into rtdocs folder:

![Move Command](/images/move_command.png)

now remove hyperledger… folder and the content:

![Compress files](/images/remove_command.png)

uncompress the file here and remove compress file:

```console
- tar -xzvf rtdocs.tar.gz
- rm rtdocs.tar.gz
```

### Install requirements

Move to the parent folder and execute the command below:

```console
pip install -r requirements.txt
```

### Activate GPU

After the requirements installation we can switch to GPU before to execute the ingestion script:

![Activate GPU](/images/activate_gpu.png)

then select the L4 solution:

![Select L4](/images/select_L4.png)

and confirm (it takes some minutes).

### Ingest step

Run the ingest.py script:

![Run Ingest](/images/run_ingest.png)

it will create content in chromadb folder.

### Run API

Now, we can run the API and test it. So, run api.py script:

![Run API](/images/run_api.png)

and test it:

```console
curl --header "Content-Type: application/json" --request POST --data '{"text": "How to install Hyperledger fabric?"}' http://127.0.0.1:8080/query
```

below the result:

![Show results](/images/curl_results.png)

## Current version notes

That is a proof-of-concept: a list of future improvement below:

1. This is the first version of the prototype and it will be installed on a GPU Cloud Server
2. At the same time, we'd like to pass to the next step: the Hyperledger Incubation Stage
3. We will investigate other open source models
4. Evaluation of the system using standard metrics
5. We would like to improve the system, some ideas are: fine-tuning, Advanced RAG, Decomposed LoRA
6. Add "guardrails" which are a specific ways of controlling the output of a LLM, such as talking avoid specific topics, responding in a particular way to specific user requests, etc.

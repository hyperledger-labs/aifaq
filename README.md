# Hyperledger QA PoC version 2

The scope of this Hyperledger Labs project is to support the users (users, developer, etc.) to their work, avoiding to wade through oceans of documents to find information they are looking for. We are implementing an open source conversational AI tool which replies to the questions related to specific context. This is a proof-of-concept software which allows to create a chatbot using Google Colab (or local notebook which requires GPU). Here the official Wiki page: [Hyperledger Labs aifaq](https://labs.hyperledger.org/labs/aifaq.html). Please, read also the [Antitrust Policy and the Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). The meeting invitation is on the Hyperledger Labs calendar: [[Hyperledger Labs] FAQ AI Lab calls](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

## Background

The system is an open source Jupyter Notebook (derived from here [medium.com](https://levelup.gitconnected.com/building-a-private-ai-chatbot-2c071f6715ad)) which implements an AI chatbot. The idea is to implement an open source framework/template, as example, for other communities. Last results in open LLMs allow to have good performance using common HW resources.\
Below the application architecture:

![LLM chatbot schema](/images/poc_schema_v2.png)

We use RAG (Retrieval Augmented Generation [arxiv.org](https://arxiv.org/abs/2312.10997)) for question answering use case. That technique aims to improve LLM answers by incorporating knowledge from external database (e.g. vector database).

The image depicts two workflow:

1. The data ingestion workflow
2. The chat workflow

During the ingestion phase, the system loads context documents and creates a vector database. In our case, the document sources are:

- An online software guide (readthedocs template)
- The GitHub issues and pull requests

After the first phase, the system is ready to reply to user questions.

Currently, we use the open source [HuggingFace Zephyr-7b-alpha](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha). But, in the future we want to investigate other open source models. Moreover, the User Interface uses [Gradio](https://www.gradio.app/).

## Open Source Version

The software is under Apache 2.0 License (please check LICENSE and NOTICE files included). For the dependencies, it is [ASF 3rd Party License Policy](https://www.apache.org/legal/resolved.html) compliant: the **LICENSE** file contains "pointers" to the dependency's licenses and a list of Apache 2.0-licensed dependecies ([Assembling LICENSE and NOTICE files](https://infra.apache.org/licensing-howto.html#mod-notice)).

## Installation

Below the main steps to set up the system:

1. Download the **hyperledger_aifaq_poc_v3.ipynb** notebook file from the **src** folder
2. Create a new Google Colab notebook
3. Load the downloaded notebook file
4. Set up the runtime GPU
5. Copy the ReadTheDocs on Google Drive
6. Set up the Google Drive mount path
7. Set the URL and GitHub repo document sources
8. Create a new GitHub personal token
9. Add the token, as new secret, to the Google Colab notebook

The first step is straightforward: just click the **src** folder to open it, then click the **hyperledger_aifaq_poc_v3.ipynb** file and the click the button below:

![download button](/images/download_notebook_file.png)

Now, in Google Drive click on **New** button -> **Other** and **Google Colaboratory**

![new Google Colab notebook](/images/new_colab_notebook.png)

Inside the new notebook, select the **File** menu, then select **Load notebook** and then click on the "Browse" button and select the downloaded file (hyperledger_aifaq_poc_v3.ipynb).

We need a GPU to execute the notebook. So, we can set it up from the **Runtime** menu, then change runtime:

![set up the runtime](/images/runtime_type.png)

If you have a free account you can use only the T4 GPU.

Now, download the on-line ReadTheDocs documentation, e.g. from [Hyperledger fabric ReadTheDocs](https://hyperledger-fabric.readthedocs.io/en/release-2.5/):

Click on the **v: realease-2.5** and then click on Download:

![readthedocs](/images/readthedocs.png)

It should open a web page where it is possible to download the HTML version:

![download readthedocs](/images/download_rtdocs.png)

Unzip the file and copy folders and files on your Google Drive:

![google drive readthedocs](/images/gdrive_rtdocs.png)

Now, we can set the document sources. The notebook takes the documents for RAG from three sources:

1. An online website
2. A local ReadTheDocs documentation
3. A GitHub repository

The image below shows how to set them up:

![document sources](/images/set_document_sources.png)

In our case, we get the **Hyperledger fabric** wiki page and its GitHub repository (getting issues and pull requests).
Into **url** string we specify the website, while in **repo** string we set the GitHub repository.\\

While, we should specify the ReadTheDocs **folderpath** and use it below.

From your personal GitHub account, inside the profile settings, select the developer settings:

![developer settings](/images/developer_settings.png)

Then select the **fine-grained token**

![fine-grained token](/images/fine_grained_token.png)

and click on the generate button: now copy the token.\\
Into the Google Colab notebook, select the **secret key** and add a new secret, like the image below:

![github personal token](/images/github_personal_token.png)

- The token must have the access to the notebook
- The name should be **GITHUB_PERSONAL_ACCESS_TOKEN**
- Past it inside the **Value** field

## Usage

Now, we can test the PoC by executing the notebook: in Google Colab notebook -> **Runtime menu**, select **Execute all**:

- It will take 5-15 minutes (it depends on the GPU and the documents)
- When the execution finishes, it loads an UI which allows to ask questions and replies in around 30 seconds

Below an example:

![UI Gradio example](/images/ui_gradio_question.png)

For any reason, please, contact us on Discord Channel:

- Server: Hyperledger
- Channel: #aifaq

## Current version notes

That is a proof-of-concept: a list of future improvement below:

1. We want to implement a prototype starting from that PoC: container architecture installed on a GPU Cloud Server
2. At the same time, we'd like to pass to the next step: the Hyperledger Incubation Stage
3. We will investigate other open source models
4. Evaluation of the system using standard metrics
5. We would like to improve the system, some ideas are: fine-tuning, Corrective RAG, Decomposed LoRA
6. Add "guardrails" which are a specific ways of controlling the output of a LLM, such as talking avoid specific topics, responding in a particular way to specific user requests, etc.

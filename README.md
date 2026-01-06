
![Hyperledger Labs](https://img.shields.io/badge/Hyperledger-Labs-blue?logo=hyperledger)
![Apache License 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg?logo=python)

[![GitHub Stars](https://img.shields.io/github/stars/hyperledger-labs/aifaq?style=social)](https://github.com/hyperledger-labs/aifaq/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/hyperledger-labs/aifaq?style=social)](https://github.com/hyperledger-labs/aifaq/network/members)
[![Issues](https://img.shields.io/github/issues/hyperledger-labs/aifaq)](https://github.com/hyperledger-labs/aifaq/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/hyperledger-labs/aifaq)](https://github.com/hyperledger-labs/aifaq/pulls)


# Hyperledger Labs AIFAQ Prototype in Snowflake 
An Open-Source Conversational AI - Intelligence App built on Snowflake Cloud Environment

## Overview

The **Hyperledger Labs AIFAQ Prototype** is an open-source conversational intelligence system designed to deliver accurate, context-aware answers from enterprise documentation, technical references, and organizational knowledge bases. It integrates the governance strengths of Hyperledger with the scalability of **Snowflake** and the flexibility of **open-source LLMs** to create a secure, multi-tenant production grade enterprise knowledge assistant.

The prototype demonstrates a complete pipeline for ingesting, embedding, storing, and querying documents using Snowflake’s native capabilities and external AI inference. It supports open models such as **Llama**, **Mistral**, and **Snowflake Arctic** etc, offering a modular architecture suitable for production-grade deployments.

## Features

- **Multi-User Authentication**  
  Secure login and strict data isolation across document sets and chat histories.

- **Hybrid LLM Support**  
  Route queries to Snowflake Cortex or external OpenSource LLM models through secure external functions.

- **Multi-Document Knowledge Retrieval**  
   Supports structured and unstructured data.

- **Persistent Chat Sessions**  
  Full session history stored in Snowflake with easy retrieval.

- **Streamlit Frontend**  
  Intuitive UI for uploading documents, interacting with the assistant, and browsing past conversations.

- **Snowflake Vector Search**  
  High-performance similarity search using Cortex Vector Search and SQL APIs inside the snowflake cloud environment.

- **Automated Pipelines**  
  Re-embedding and re-indexing triggered by Snowflake Streams and Tasks when documents update.

- **Enterprise Governance**  
  RBAC, row-level security, and masking policies ensure protected data access.


## Architecture

### 1. Ingestion Layer
- Accepts structured and unstructured formats including PDFs, HTML, plain text, and transcripts.  
- Uses Snowflake external tables, stages, Snowpipe, or cloud functions to store and extract metadata.  
- All raw inputs move through well-defined staging schemas.

### 2. Preprocessing & Embedding
- Snowpark UDFs handle chunking, cleaning, and tokenization.  
- Embeddings generated using Cortex or external open-source models.  
- Metadata and embedding vectors stored inside Snowflake as the unified knowledge base.

### 3. Access Control & Security
- Document and chat isolation enforced via Snowflake roles.  
- Row-level security restricts user visibility to their own data.  
- Sensitive fields are masked using policy-based governance.

### 4. Retrieval-Augmented Generation (RAG)
- User query → vector search → relevant context retrieval → model response.  
- Hybrid routing selects the best LLM based on context given by the user preference.  
- Ensures responses are grounded in user-provided documentation.

### 5. Automation & Observability
- Snowflake Streams detect document changes.  
- Tasks automate reprocessing and embedding updates.  
- Monitoring through Snoopy and event notifications for operational visibility.

---

## Getting Started

1. Choose the appropriate implementation folder:  
   - **version_1** for stable production deployment 
   - **version_2** for advanced workflows with Multi cloud data ingestion

2. Follow the README inside the selected folder to set up:  
   - Warehouses  
   - Stages and schemas  
   - Pipelines  
   - External LLM functions  
   - Streamlit deployment  
---

## Folder Descriptions

### `version_1/` 
A simplified demonstration build intended for quick snowflake evaluation and to get hands on for beginners.

Includes:
- Lightweight ingestion + embedding flow  
- Basic Streamlit UI  
- Environment dependencies 
- Minimal Snowflake setup scripts 
- Ingestion and RAG flows   

---

### `version_2/`
A more advanced, optimized version improving modularity and performance.

Includes:
- Refined RAG pipeline  ( Improved data ingestion pipeline)
- Cortex Vector Search & utilities  
- Advanced version of Role Base Access Control (RBAC)  
- Enhanced logging/observability  
- Stronger multi-tenant isolation  
- Updated Streamlit interface  
- Multi Cloud ingestion

---



## 🌐 Open Source License

- **License:** Apache 2.0 (see [`LICENSE`](./LICENSE) and [`NOTICE`](./docs/NOTICE))
- **3rd Party Libraries:** [ASF 3rd Party License Policy](https://www.apache.org/legal/resolved.html)
- **License Assembly:** [Assembling LICENSE and NOTICE](https://infra.apache.org/licensing-howto.html#mod-notice)


## 🤝 Contributing

We welcome contributions! Please check our [CONTRIBUTING](./docs/CONTRIBUTING.md) guidelines and [Antitrust Policy and Code of Conduct](https://lf-hyperledger.atlassian.net/wiki/spaces/HIRC/pages/19169404/Anti-trust+Policy+Notice+Code+of+Conduct).


## 📆 Join Us!

Join our weekly public calls every Monday! See the [Hyperledger Labs Calendar](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings) for details.


## Stay Connected

- [Slack Discussions](https://join.slack.com/t/aifaqworkspace/shared_invite/zt-337k74jsl-tvH_4ct3zLj99dvZaf9nZw)
- [Hyperledger Labs Community](https://lf-hyperledger.atlassian.net/wiki/spaces/labs/pages/20290949/AI+FAQ+2025)
- Official Website: [aifaq.pro](https://aifaq.pro)
- Official Wiki Pages: [Hyperledger Labs Wiki](https://lf-hyperledger.atlassian.net/wiki/spaces/labs/pages/20290949/AI+FAQ+2025)

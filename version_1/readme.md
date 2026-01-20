# Version 1  (Step-by-Step Guide)

This repository provides a **minimal, end-to-end guide** to deploy and test the **AIFAQ chatbot version 1** on **Snowflake Cloud** using **Snowflake Cortex** and **Streamlit** ( This test project folder is designed to be beginner-friendly and introduces users to Cortex AI on the Snowflake cloud ).

The goal is to help you quickly validate the system using Snowflake’s free trial credits and run a **document-aware, context-based chatbot** with minimal setup.

---

## Overview

This implementation consists of **two core files**:

- **`setup.sql`** - Provisions all required Snowflake infrastructure (warehouse, database, schemas, tables, roles, etc.)
- **`app.py`** - Streamlit application that runs entirely inside Snowflake and uses Cortex LLMs for answering questions from uploaded documents

---

## Prerequisites

### 1. Create a Snowflake Account

- Create a Snowflake account from the official website.
- Snowflake typically provides **free trial credits** (commonly **$300–$400**, depending on region and time).
- These credits are sufficient to fully test this repository.

### 2. Select the Cloud Provider

When creating the account, select one of the following:

- ✅ **AWS**
- ✅ **Azure**
- ❌ **GCP** (Snowflake Cortex AI is **not supported on GCP at the time of writing**)

Choosing AWS or Azure avoids unnecessary complexity in later steps.

---

## Step 1: Log in to Snowflake (Snowsight UI)

1. Log in to your Snowflake account.
2. You will land on the **Snowsight Dashboard**.
3. From the left sidebar, open **Worksheets**.

---

## Step 2: Verify Snowflake Cortex Availability

Before running anything in the worksheets, confirm that **Cortex AI functions** are available in your account region.

### Check Cortex LLM availability:
- https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql#label-cortex-llm-availability

This page shows:
- Which regions support Cortex
- Which LLMs are available in each region

### If Cortex is NOT available in your region

If your account was created in a region without Cortex support:

1. Follow the **Cross-Region Inference** guide:
   - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference
2. Use `ALTER ACCOUNT` to enable inference in a supported region.
3. This step is **mandatory** for the app to work.

---

## Step 3: Run `setup.sql` (Infrastructure Setup)

1. In **Snowsight**, click **+ Worksheet** → **SQL Worksheet**
2. A new SQL file is created automatically.
3. Copy the **entire contents** of `setup.sql` from this repository.
4. Paste it into the worksheet.
5. **Run all statements**.

This script will:
- Create the required **warehouse**
- Create the **database and schemas**
- Create all necessary **tables**
- Configure permissions needed for the Streamlit app

Once this completes successfully, the Snowflake-side infrastructure is ready.

---

## Step 4: Create the Streamlit App in Snowflake

1. In **Snowsight**, go to:
   - **Projects** → **Streamlit**
2. Click **Create Streamlit App**
3. When prompted, select:
   - **Warehouse** → the one created in `setup.sql`
   - **Database** → the one created in `setup.sql`
   - **Schema** → as defined in `setup.sql`

Snowflake will create a default file called: **streamlit_app.py**


---

## Step 5: Add the Application Code (`app.py`)

1. Open the newly created **`streamlit_app.py`** file in Snowsight.
2. Delete the default contents.
3. Copy the full contents of **`app.py`** from this repository.
4. Paste it into `streamlit_app.py`.
5. Save the file.

---

## Step 6: Install Python Dependencies

Snowflake Streamlit apps require **manual dependency installation**.
There is **no automatic `requirements.txt` resolution**, so all libraries must be added explicitly.

### Steps

1. In the Streamlit app UI, open **Python Packages / Environment**.
2. Select the required **Python version**.
3. Add the following libraries **one by one**:

### Required Python Libraries

* `streamlit`
* `snowflake-snowpark-python`
* `pandas`
* `pypdf`
* `python-pptx`
* `openpyxl`
* `xlrd` *(required only for legacy `.xls` Excel files)*

> ⚠️ **Do NOT add** built-in Python modules such as `uuid`, `re`, `datetime`, `io`, or `time`.

4. After adding all libraries, **save** the environment.

Snowflake will automatically **reinitialize the app** once the environment is updated.


### Validation Checklist

* PDF uploads work → `pypdf` installed
* PowerPoint uploads work → `python-pptx` installed
* Excel uploads work → `openpyxl` (and `xlrd` if `.xls`) installed
* Snowflake Cortex / Snowpark works → `snowflake-snowpark-python` installed

---

## Step 7: Run and Test the Chatbot

You are now ready to test the system.

### What you can do in the UI:
- Upload documents in formats such as:
  - PDF
  - TXT
  - CSV
  - DOCX
- Ask natural-language questions about the uploaded documents
- Receive **context-aware answers** powered by **Snowflake Cortex LLMs**

The chatbot:
- Retrieves relevant document context
- Uses Cortex AI functions for reasoning
- Responds conversationally through Streamlit

---

## What This Setup Demonstrates

- End-to-end AIFAQ deployment inside Snowflake
- Snowflake-native Streamlit application
- Secure document ingestion and querying
- LLM-powered question answering using Cortex
- Zero external infrastructure required

---

## Notes & Limitations

- Cortex availability is **region-dependent**
- GCP is not supported for Cortex at the time of writing
- Dependency management in Snowflake Streamlit is manual by design
- Trial credits are limited; monitor usage

---

## Next Steps

- Extend authentication and user isolation
- Add vector search optimizations
- Integrate additional LLMs available in Cortex
- Productionize with role-based access controls

---

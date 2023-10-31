import json
import glob as glob
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (containing Elastich Search config and credentials)
load_dotenv()

PASSWORD=os.environ.get("PASSWORD")

BASEPATH = './ingest'
# file in Elastic Search format
dataset_path = BASEPATH + "faq_es_format_v3"

# create Elastic Search Document Store connecting to local service
from haystack.document_stores import ElasticsearchDocumentStore
document_store = ElasticsearchDocumentStore(host="localhost", port=9200, username="elastic", password=PASSWORD, scheme="https", verify_certs=False, return_embedding=True)

# read all file in Elastic Search format
es_files = glob.glob(dataset_path + "*")
# loop files
for file in es_files:
    # create a dictionary using file in Elastic Search format
    es_dict = {}
    with open(file, "r", encoding="utf8") as f:
        es_dict = json.load(f)
    # write data in Document Store
    document_store.write_documents(es_dict, index="document")    
    

# create the Retriever of documents
from haystack.nodes.retriever import BM25Retriever
bm25_retriever = BM25Retriever(document_store=document_store)

# create the Reader of documents
from haystack.nodes import FARMReader
#alternative models: deepset/roberta-base-squad2-distilled or deepset/xlm-roberta-large-squad2 or the tiny distilled model: deepset/tinyroberta-squad2
model_ckpt = "deepset/xlm-roberta-large-squad2"
max_seq_length, doc_stride = 384, 128
reader = FARMReader(model_name_or_path=model_ckpt, progress_bar=False, max_seq_len=max_seq_length, doc_stride=doc_stride, return_no_answer=False)

# create the pipeline
from haystack.pipelines import ExtractiveQAPipeline
pipe = ExtractiveQAPipeline(reader=reader, retriever=bm25_retriever)

# file in SQuAD format
dataset_path_squad = "faq_squad_format.json"
# fine-tuning of pre-trained model
reader.train(data_dir=BASEPATH, use_gpu=False, n_epochs=1, batch_size=16, train_filename=dataset_path_squad)

# loop while user does not write "exit"
while True:
    # read the questio from user prompt
    query = input("Ask me something about Hyperledger documentation? \n\n")

    # stop the loop if user write "exit"
    if query == "exit":
        break

    item_id = "hl1"
    # number of output answers 
    n_answers = 1
    # answers prediction
    preds = pipe.run(query=query, params={"Retriever": {"top_k": 3}, "Reader": {"top_k": n_answers}})

    # print the question
    print(f"Question: {preds['query']} \n")

    # print the answers and the snippet of the text
    for idx in range(n_answers):
        print(f"Answer {idx+1}: {preds['answers'][idx].answer}")
        print(f"Text snippet: ...{preds['answers'][idx].context}...")
        print("\n\n")

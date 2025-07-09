import os
import time
from os.path import isfile, join
from os import listdir
from utils import load_yaml_file, bs4_extract_linear_text, extract_video_id, save_transcript, bs4_lxml_improved
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import BSHTMLLoader

def check_file_exists_and_valid(file_path, min_size=100):
    """Check if file exists and has minimum size (basic validation)"""
    return os.path.exists(file_path) and os.path.getsize(file_path) >= min_size

def process_youtube_links_with_retry(dataset_dir, config_data, max_retries=3, retry_delay=2):
    """Process YouTube links with retry logic"""
    folder_pth = join(dataset_dir, config_data["yt_video_links"])
    yt_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]
    
    failed_downloads = []
    successful_downloads = []
    
    # First pass: try to download all videos
    for file in yt_files:
        fpath = os.path.join(folder_pth, file)
        with open(fpath, 'r', encoding='UTF-8') as f:
            for line_num, line in enumerate(f, 1):
                url = line.strip()
                if not url:
                    continue
                    
                video_id = extract_video_id(url)
                if not video_id:
                    print(f"Could not extract video ID from: {url}")
                    continue
                
                out_path = os.path.join(folder_pth, "transcripts")
                os.makedirs(out_path, exist_ok=True)
                transcript_file = os.path.join(out_path, f"{video_id}.txt")
                
                try:
                    save_transcript(video_id, out_path)
                    if check_file_exists_and_valid(transcript_file):
                        successful_downloads.append((url, video_id, transcript_file))
                        print(f"✓ Downloaded transcript for: {url}")
                    else:
                        failed_downloads.append((url, video_id, transcript_file, file, line_num))
                except Exception as e:
                    print(f"✗ Failed to download {url}: {str(e)}")
                    failed_downloads.append((url, video_id, transcript_file, file, line_num))
    
    # Retry failed downloads
    retry_count = 0
    while failed_downloads and retry_count < max_retries:
        retry_count += 1
        print(f"\n--- Retry attempt {retry_count}/{max_retries} for {len(failed_downloads)} failed downloads ---")
        
        still_failed = []
        for url, video_id, transcript_file, source_file, line_num in failed_downloads:
            print(f"Retrying: {url} (from {source_file}:{line_num})")
            time.sleep(retry_delay)  # Add delay between retries
            
            try:
                out_path = os.path.dirname(transcript_file)
                save_transcript(video_id, out_path)
                
                if check_file_exists_and_valid(transcript_file):
                    successful_downloads.append((url, video_id, transcript_file))
                    print(f"✓ Retry successful for: {url}")
                else:
                    still_failed.append((url, video_id, transcript_file, source_file, line_num))
            except Exception as e:
                print(f"✗ Retry failed for {url}: {str(e)}")
                still_failed.append((url, video_id, transcript_file, source_file, line_num))
        
        failed_downloads = still_failed
        if retry_delay < 10:  # Increase delay for subsequent retries
            retry_delay += 1
    
    # Report final results
    print(f"\n=== YouTube Processing Summary ===")
    print(f"Successful downloads: {len(successful_downloads)}")
    print(f"Failed downloads: {len(failed_downloads)}")
    
    if failed_downloads:
        print("\nPersistent failures:")
        for url, video_id, transcript_file, source_file, line_num in failed_downloads:
            print(f"  - {url} (from {source_file}:{line_num})")
    
    return successful_downloads, failed_downloads

def process_web_urls_with_retry(dataset_dir, config_data, max_retries=3, retry_delay=2):
    """Process web URLs with retry logic"""
    folder_pth = join(dataset_dir, config_data["web_urls"])
    web_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]
    
    successful_loaders = []
    failed_urls = []
    
    for file in web_files:
        fpath = os.path.join(folder_pth, file)
        with open(fpath, 'r', encoding='UTF-8') as f:
            for line_num, line in enumerate(f, 1):
                url = line.strip()
                if not url:
                    continue
                
                success = False
                last_error = None
                
                for attempt in range(max_retries + 1):
                    try:
                        if attempt > 0:
                            print(f"Retrying URL (attempt {attempt + 1}): {url}")
                            time.sleep(retry_delay * attempt)
                        
                        loader = RecursiveUrlLoader(
                            url=url, 
                            extractor=bs4_lxml_improved, 
                            prevent_outside=True,
                            max_depth=1
                        )
                        # Test the loader by trying to load one document
                        test_docs = loader.load()
                        if test_docs:
                            successful_loaders.append(loader)
                            print(f"✓ Successfully processed URL: {url}")
                            success = True
                            break
                        else:
                            raise Exception("No documents loaded from URL")
                            
                    except Exception as e:
                        last_error = str(e)
                        if attempt == max_retries:
                            print(f"✗ Failed to process {url} after {max_retries + 1} attempts: {last_error}")
                            failed_urls.append((url, file, line_num, last_error))
    
    print(f"\n=== Web URL Processing Summary ===")
    print(f"Successful URLs: {len(successful_loaders)}")
    print(f"Failed URLs: {len(failed_urls)}")
    
    return successful_loaders, failed_urls

def get_vectordb(owner: str, access: str, datasetdir: str):
    """Enhanced version with retry logic for downloads"""
    config_data = load_yaml_file("config.yaml")
    
    # Get retry parameters from config, with defaults
    max_retries = config_data.get("max_download_retries", 3)
    retry_delay = config_data.get("retry_delay_seconds", 2)
    
    # Load environment variables
    load_dotenv(find_dotenv())
    
    dataset_dir = datasetdir
    
    print("=== Starting Enhanced Ingestion Process ===\n")
    
    # Process YouTube videos with retry logic
    print("Processing YouTube videos...")
    successful_yt, failed_yt = process_youtube_links_with_retry(
        dataset_dir, config_data, max_retries, retry_delay
    )
    
    # Create YouTube loaders from successful downloads
    yt_list = []
    out_path = os.path.join(dataset_dir, config_data["yt_video_links"], "transcripts")
    if os.path.exists(out_path) and successful_yt:
        text_loader_kwargs = {'autodetect_encoding': True}
        yt_list = DirectoryLoader(
            out_path, 
            glob="*", 
            loader_cls=TextLoader, 
            show_progress=True, 
            loader_kwargs=text_loader_kwargs
        )
    
    # Process web URLs with retry logic
    print("\nProcessing web URLs...")
    web_list, failed_web = process_web_urls_with_retry(
        dataset_dir, config_data, max_retries, retry_delay
    )
    
    # Process PDF files (existing logic)
    print("\nProcessing PDF files...")
    folder_pth = join(dataset_dir, config_data["pdf_files"])
    pdf_list = GenericLoader(
        blob_loader=FileSystemBlobLoader(
            path=folder_pth,
            glob="*.pdf",
        ),
        blob_parser=PyPDFParser(),
    )
    
    # Process HTML files (existing logic with error handling)
    print("Processing HTML files...")
    html_list = []
    folder_pth = join(dataset_dir, config_data["html_files"])
    if os.path.exists(folder_pth):
        html_files = [file for file in listdir(folder_pth) if isfile(join(folder_pth, file))]
        
        for file in html_files:
            fpath = os.path.join(folder_pth, file)
            try:
                loader = BSHTMLLoader(fpath, open_encoding='utf-8')
                html_list.append(loader)
                print(f"✓ Loaded HTML file: {file}")
            except Exception as e:
                print(f"✗ Failed to load HTML file {fpath}: {str(e)}")
    
    # Process ReadTheDocs files (existing logic)
    print("Processing ReadTheDocs files...")
    folder_pth = join(dataset_dir, config_data["rtdocs_files"])
    rtdocs_list = None
    if os.path.exists(folder_pth):
        rtdocs_list = ReadTheDocsLoader(folder_pth, encoding="utf-8")
    
    # Process text files (existing logic)
    print("Processing text files...")
    folder_pth = join(dataset_dir, config_data["text_files"])
    text_loader_kwargs = {'autodetect_encoding': True}
    txt_list = DirectoryLoader(
        folder_pth, 
        glob="*", 
        loader_cls=TextLoader, 
        show_progress=True, 
        loader_kwargs=text_loader_kwargs
    )
    
    # Combine all loaders
    loaders = []
    
    # Add web loaders
    loaders.extend(web_list)
    
    # Add HTML loaders
    loaders.extend(html_list)
    
    # Add other loaders
    loaders.append(pdf_list)
    if rtdocs_list:
        loaders.append(rtdocs_list)
    if yt_list:
        loaders.append(yt_list)
    loaders.append(txt_list)
    
    if not loaders:
        print("⚠️  No loaders available - no documents will be processed")
        return None
    
    # Merge all document sources
    print(f"\nMerging {len(loaders)} document sources...")
    loader = MergedDataLoader(loaders=loaders)
    
    # Load data
    print("Loading documents...")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    
    # Set document metadata
    for doc in docs:
        doc.metadata.update({'owner': owner, 'access': access})
    
    # Split text into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    print(f"Created {len(documents)} text chunks")
    
    # Get API keys
    mistral_api_key = os.getenv("MISTRALAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Select embeddings based on provider
    print(f"Using {config_data['llm_provider']} embeddings...")
    if config_data["llm_provider"] == "mistral":
        embeddings = MistralAIEmbeddings(
            model=config_data["embedding_model"], 
            mistral_api_key=mistral_api_key
        )
    else:  # default to OpenAI
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    if documents:
        # Create the vector store
        print("Creating vector database...")
        vectordb = FAISS.from_documents(documents, embeddings)
        
        # Print final summary
        print(f"\n=== Ingestion Complete ===")
        print(f"Total documents processed: {len(docs)}")
        print(f"Total text chunks: {len(documents)}")
        print(f"YouTube failures: {len(failed_yt)}")
        print(f"Web URL failures: {len(failed_web)}")
        
        if failed_yt or failed_web:
            print(f"\n⚠️  Some downloads failed. Check logs above for details.")
            
        return vectordb
    else:
        print("✗ No documents were successfully processed")
        return None

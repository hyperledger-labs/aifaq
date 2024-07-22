import os
import subprocess
import shutil
from urllib.parse import urlparse
import time
from utils import load_yaml_file

def download_content(urls, folder_path):
    """Downloads content from a list of URLs using wget."""
    for url in urls:
        parsed_url = urlparse(url)
        base_path = parsed_url.path.strip('/').replace('/', '_')
        download_path = os.path.join(folder_path, base_path)
        wget_command = [
            'wget',
            '-r',                   
            '-np',                 
            '-k',                  
            '-p',                  
            '--no-check-certificate', 
            '--recursive',         
            '--level=inf',          
            '--accept=html',       
            '-P', download_path,    
            url
        ]
        print(f"Downloading content from {url}...")
        try:
            result = subprocess.run(wget_command, check=False, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            print(f"An error occurred while running wget for {url}: {e}")

def count_downloaded_files(base_path):
    """Counts the number of files downloaded in the base path."""
    try:
        count = sum([len(files) for r, d, files in os.walk(base_path)])
        print(f"Number of files downloaded: {count}")
    except Exception as e:
        print(f"An error occurred while counting files in {base_path}: {e}")
    time.sleep(5)  


def reorganize_files(src_path, dst_path):
    """Moves files from the source directory to the destination directory and removes empty directories."""
    print(f"Checking source path: {src_path}")
    if not os.path.exists(src_path):
        print(f"Error: The source directory {src_path} does not exist.")
        return False
    print("Moving files...")
    try:
        for root, _, files in os.walk(src_path):
            for file in files:
                s = os.path.join(root, file)
                base, ext = os.path.splitext(file)
                counter = 1
                d = os.path.join(dst_path, file)
                while os.path.exists(d):
                    d = os.path.join(dst_path, f"{base}_{counter}{ext}")
                    counter += 1
                
                print(f"Moving {s} to {d}")
                shutil.move(s, d)
        print("Removing empty directory structure...")
        shutil.rmtree(src_path)
        return True
    except Exception as e:
        print(f"An error occurred while moving files: {e}")
        return False

def count_total_files(folder_path):
    """Counts the total number of files in the specified folder."""
    try:
        count = sum([len(files) for r, d, files in os.walk(folder_path)])
        print(f"Total number of files in {folder_path}: {count}")
    except Exception as e:
        print(f"An error occurred while counting total files in {folder_path}: {e}")

def main():
    config = load_yaml_file('config.yaml')
    urls = config.get('doclinks', [])
    folder_path = config.get('folder_path', 'rtdocs')
    if urls:
        for url in urls:
            try:
                parsed_url = urlparse(url)
                base_path = parsed_url.path.strip('/').replace('/', '_')
                download_path = os.path.join(folder_path, base_path)
                download_content([url], folder_path)
                count_downloaded_files(download_path)
                if reorganize_files(download_path, folder_path):
                    print(f"Success: Content from {url} downloaded and reorganized successfully.")
                else:
                    print(f"Download completed for {url}, but file reorganization failed.")
            except Exception as e:
                print(f"An error occurred while processing {url}: {e}")
            count_total_files(folder_path)        
    else:
        print("No URLs found in config.yaml.")

if __name__ == "__main__":
    main()



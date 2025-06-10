#!/usr/bin/env python3
# filepath: create_directories.py

import os

def create_directories():
    """Create directory structure for AIFAQ project"""
    
    directories = [
        # Public dataset directories
        "./dataset/public/web_urls",
        "./dataset/public/yt_video_links/transcripts",
        "./dataset/public/text_files",
        "./dataset/public/pdf_files",
        "./dataset/public/rtdocs_files",
        "./dataset/public/html_files",
        
        # Private dataset directories
        "./dataset/private/web_urls",
        "./dataset/private/yt_video_links/transcripts",
        "./dataset/private/text_files",
        "./dataset/private/pdf_files",
        "./dataset/private/rtdocs_files",
        "./dataset/private/html_files",
        
        # Other directories
        "./faiss_index",
        "./rtdocs"
    ]
    
    # Create each directory
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")

if __name__ == "__main__":
    # Directories must be created in src/mvt
    print("Creating directories for AIFAQ project...")
    create_directories()
    print("Directory creation complete!")
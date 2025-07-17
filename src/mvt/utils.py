import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
import re
from urllib.parse import urlparse, parse_qs
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# This file contains utility functions for the MVT project.
# It includes functions for loading YAML files, extracting text from HTML using BeautifulSoup,
# and converting emojis to Unicode format.
def load_yaml_file(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def load_yaml_file_with_db_prompts(path):
    """Load YAML file and override prompts with database values if available"""
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    # Try to load prompts from database
    try:
        from database import create_connection, get_prompt
        conn = create_connection()
        if conn:
            # Get prompts from database
            db_system_prompt = get_prompt(conn, "system_prompt")
            db_query_rewriting_prompt = get_prompt(conn, "query_rewriting_prompt")
            
            # Override config values if database values exist
            if db_system_prompt:
                data["system_prompt"] = db_system_prompt
            if db_query_rewriting_prompt:
                data["query_rewriting_prompt"] = db_query_rewriting_prompt
            
            conn.close()
    except Exception as e:
        # If database loading fails, use config defaults
        print(f"Warning: Could not load prompts from database: {e}")
    
    return data

# This function returns the system prompt from the file specified in the config.
def get_prompt_from_file(prompt_file: str):
    with open(prompt_file, "r") as f:
        return f.read().strip()



# This function extracts text from HTML while preserving context relationships.
def bs4_html(html):
    """Extract text from HTML while preserving context relationships"""
    soup = BeautifulSoup(html, "html.parser")
    ex_data = []

    # Find main content blocks including divs with specific text content
    main_blocks = soup.find_all(
        ["div", "section", "article"],
        class_=lambda x: x and any(word in str(x).lower() for word in ['content', 'main', 'about', 'mission'])
    )

    for block in main_blocks:
        # First check for div elements that might be headers
        divs = block.find_all('div')
        for div in divs:
            div_text = div.get_text(strip=True)
            if div_text and div_text.isupper() and len(div_text) < 30:  # Likely a header like "MISSION"
                content_parts = []
                next_elem = div.find_next_sibling()
                while next_elem and not (next_elem.name == 'div' and next_elem.get_text(strip=True).isupper()):
                    if next_elem.get_text(strip=True):
                        content_parts.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                if content_parts:
                    combined_text = f"{div_text}\n{' '.join(content_parts)}"
                    ex_data.append(combined_text)
        
        headings = block.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            heading_text = heading.get_text(strip=True)
            if heading_text:
                # Find the next sibling elements until we hit another heading
                content_parts = []
                next_elem = heading.find_next_sibling()
                while next_elem and not next_elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if next_elem.get_text(strip=True):
                        content_parts.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                # Combine heading with its related content
                if content_parts:
                    combined_text = f"{heading_text}\n{' '.join(content_parts)}"
                    ex_data.append(combined_text)

        # Get remaining significant text blocks
        for p in block.find_all(['p', 'div']):
            text = p.get_text(separator=' ', strip=True)
            if len(text) > 50 and text not in ' '.join(ex_data):
                ex_data.append(text)

    return '\n\n'.join(ex_data)

def bs4_html_improved(html):
    """Extract text from HTML while preserving context relationships"""
    soup = BeautifulSoup(html, "html.parser")
    ex_data = []

    # Capture all divs with class 'elementor-heading-title' and group consecutive pairs
    heading_divs = soup.find_all('div', class_='elementor-heading-title')
    paired_items = []
    i = 0
    while i < len(heading_divs) - 1:
        key = heading_divs[i].get_text(strip=True)
        val = heading_divs[i + 1].get_text(strip=True)

        # Simple heuristic: key is text, value looks like money or a number
        if (
            key and not key.startswith('$') and
            (val.startswith('$') or val.replace(',', '').isdigit())
        ):
            combined = f"{key}: {val}"
            paired_items.append(combined)
            i += 2  # skip to next pair
        else:
            i += 1  # just move one step

    if paired_items:
        ex_data.extend(paired_items)

    # Find main content blocks including divs with specific text content
    main_blocks = soup.find_all(
        ["div", "section", "article"],
        class_=lambda x: x and any(word in str(x).lower() for word in ['content', 'main', 'about', 'mission'])
    )

    for block in main_blocks:
        # First check for div elements that might be headers
        divs = block.find_all('div')
        for div in divs:
            div_text = div.get_text(strip=True)
            if div_text and div_text.isupper() and len(div_text) < 30:  # Likely a header like "MISSION"
                content_parts = []
                next_elem = div.find_next_sibling()
                while next_elem and not (next_elem.name == 'div' and next_elem.get_text(strip=True).isupper()):
                    if next_elem.get_text(strip=True):
                        content_parts.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                if content_parts:
                    combined_text = f"{div_text}\n{' '.join(content_parts)}"
                    ex_data.append(combined_text)
        
        headings = block.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            heading_text = heading.get_text(strip=True)
            if heading_text:
                # Find the next sibling elements until we hit another heading
                content_parts = []
                next_elem = heading.find_next_sibling()
                while next_elem and not next_elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if next_elem.get_text(strip=True):
                        content_parts.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.find_next_sibling()
                
                # Combine heading with its related content
                if content_parts:
                    combined_text = f"{heading_text}\n{' '.join(content_parts)}"
                    ex_data.append(combined_text)

        # Get remaining significant text blocks
        for p in block.find_all(['p', 'div']):
            text = p.get_text(separator=' ', strip=True)
            if len(text) > 50 and text not in ' '.join(ex_data):
                ex_data.append(text)

    return '\n\n'.join(ex_data)


def bs4_extract_linear_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove non-visible content
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text with line breaks between elements
    text = soup.get_text(separator='\n', strip=True)

    # Clean up: remove empty lines and extra spaces
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)



def bs4_lxml(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

# Tags that we want to skip in the final text extraction
SKIP_TAGS = {"script", "style", "noscript", "header", "footer", "nav", "form"}

# Regex to compress spaces and empty lines
SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n{3,}")

def visible_text_nodes(el: Tag | NavigableString):
    """
    Returns only visible text nodes (filters script/style, comments, etc.)
    """
    if isinstance(el, NavigableString):
        # Avoid comments and extra spaces
        if el.parent.name not in SKIP_TAGS:
            txt = el.strip()
            if txt:
                yield txt
    elif el.name not in SKIP_TAGS:
        for child in el.contents:
            yield from visible_text_nodes(child)

def bs4_lxml_improved(html: str) -> str:
    # Convert HTML to string
    soup = BeautifulSoup(html, "lxml")

    # Removes unwanted elements completely (optional but useful)
    for tag in soup.find_all(SKIP_TAGS):
        tag.decompose()

    raw_lines = list(visible_text_nodes(soup.body or soup))
    joined = "\n".join(raw_lines)

    # Normalizes spaces and empty lines
    joined = SPACE_RE.sub(" ", joined)
    joined = BLANK_RE.sub("\n\n", joined.strip())
    return joined + "\n"


def convert_youtube_short_to_full(short_url):
    """
    Converts a short YouTube URL (youtu.be) to the full format (youtube.com/watch?v=...)
    """
    try:
        parsed_url = urlparse(short_url)
        if 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return short_url  # Return original URL if it's not a short youtu.be link
    except Exception as e:
        print(f"Error while converting URL: {e}")
        return None


def extract_video_id(youtube_url):
    """
    Extracts the video ID from a YouTube URL (short or full format).
    
    Supported formats:
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID
    - With or without additional query parameters
    """
    try:
        parsed_url = urlparse(youtube_url)
        
        # Handle short URL format
        if 'youtu.be' in parsed_url.netloc:
            return parsed_url.path.lstrip('/')
        
        # Handle full URL format
        if 'youtube.com' in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
        
        return None  # Not a recognized YouTube URL
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None


def save_transcript(video_id, output_folder):
    try:
        # Get the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript
        formatter = TextFormatter()
        testo_transcript = formatter.format_transcript(transcript)
        
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Define the file path
        file_path = os.path.join(output_folder, f"{video_id}_transcript.txt")
        
        # Save the transcript to a text file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(testo_transcript)
        
        print(f"Saved transcript in: {file_path}")
        
    except Exception as e:
        print(f"Error reading transcript: {e}")
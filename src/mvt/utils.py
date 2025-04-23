import yaml
from bs4 import BeautifulSoup

# This file contains utility functions for the MVT project.
# It includes functions for loading YAML files, extracting text from HTML using BeautifulSoup,
# and converting emojis to Unicode format.
def load_yaml_file(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

# This function extracts text from HTML using BeautifulSoup.
# It traverses through all paragraphs in the HTML and concatenates the text
# if the length of the text is greater than or equal to 50 characters.
# It returns the concatenated text.
def bs4_extractor(html):
    ex_data = ""
    soup = BeautifulSoup(html, "html.parser")
    # traverse paragraphs from soup 
    for data in soup.find_all("p"):
            # sentences longer than 50 chars
            if(len(data.get_text()) >= 50):
                 ex_data = ex_data + data.get_text()
    return ex_data
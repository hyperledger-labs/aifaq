import yaml
from bs4 import BeautifulSoup

def load_yaml_file(path):
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def bs4_extractor(html):
    ex_data = ""
    soup = BeautifulSoup(html, "html.parser")
    # traverse paragraphs from soup 
    for data in soup.find_all("p"):
            # sentences longer than 50 chars
            if(len(data.get_text()) >= 50):
                 ex_data = ex_data + data.get_text()
    return ex_data

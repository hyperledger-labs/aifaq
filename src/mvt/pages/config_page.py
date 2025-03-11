import os
from os.path import join, isfile
from utils import load_yaml_file
import streamlit as st
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.roles not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Config Page")

# Read config data
config_data = load_yaml_file("config.yaml")
# dataset folder
dataset_dir = config_data["dataset_path"]

# text files folder
txt_pth = join(dataset_dir, config_data["text_files"])

# pdf files folder
pdf_pth = join(dataset_dir, config_data["pdf_files"])

# readthedocs files folder
rtdocs_pth = join(dataset_dir, config_data["rtdocs_files"])

# yt video folder
yt_pth = join(dataset_dir, config_data["yt_video_links"])
# yt video file
ytpath = os.path.join(yt_pth, "yt_video_links.txt")

yt_content = ""
# check if the yt links file exists
if isfile(ytpath):
    file = open(ytpath, "r")
    yt_content = file.read()
    file.close()

# web urls folder
web_pth = join(dataset_dir, config_data["web_urls"])
# web urls file
wbpath = os.path.join(web_pth, "web_urls.txt")

wb_content = ""
# check if the web links file exists
if isfile(ytpath):
    file = open(wbpath, "r")
    wb_content = file.read()
    file.close()

st.header("Please, add your document sources using this form")

st.write("Current text files:")
filelist=[]
for root, dirs, files in os.walk(txt_pth):
    for file in files:
        filelist.append(file)
st.write(filelist)
      
# text file uploader
uploaded_text_files = st.file_uploader(
    "Upload text files", accept_multiple_files=True, type="txt"
)

st.write("Current Pdf files:")
filelist=[]
for root, dirs, files in os.walk(pdf_pth):
    for file in files:
        filelist.append(file)
st.write(filelist)

# pdf file uploader
uploaded_pdf_files = st.file_uploader(
    "Upload PDF files", accept_multiple_files=True, type="pdf"
)

st.write("Current ReadTheDocs files:")
filelist=[]
for root, dirs, files in os.walk(rtdocs_pth):
    for file in files:
        filelist.append(file)
st.write(filelist)

# rtdocs file uploader
uploaded_rtdocs_files = st.file_uploader(
    "Upload ReadTheDocs files", accept_multiple_files=True, type="html", help="Upload HTML files"
)

with st.form("sources_form"):
   if len(yt_content) != 0:
      yt_video_links = st.text_area("Youtube video links", value=yt_content)
   if len(wb_content) != 0:
      web_links = st.text_area("Web urls", value=wb_content)
   submit = st.form_submit_button('Save')

# save button click
if submit:

  with open(ytpath, "w") as file:
      print(yt_video_links.rstrip(), file=file)
      file.close()

  with open(wbpath, "w") as file:
      print(web_links.rstrip(), file=file)
      file.close()
    
  for uploaded_file in uploaded_text_files:
    # txt file
    txtfile_path = os.path.join(txt_pth, uploaded_file.name)
    with open(txtfile_path, "wb") as f:
       f.write(uploaded_file.getbuffer())
  
  for uploaded_file in uploaded_pdf_files:
    # pdf file
    pdffile_path = os.path.join(pdf_pth, uploaded_file.name)
    with open(pdffile_path, "wb") as f:
       f.write(uploaded_file.getbuffer())

  for uploaded_file in uploaded_rtdocs_files:
    # rtdoc html file
    rtdocfile_path = os.path.join(rtdocs_pth, uploaded_file.name)
    with open(rtdocfile_path, "wb") as f:
       f.write(uploaded_file.getbuffer())  
  
  st.rerun()  
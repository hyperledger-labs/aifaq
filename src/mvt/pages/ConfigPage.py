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


st.markdown(
    "Lorem ipsum dolor sit amet. Et nulla sint ea tempora iste qui eligendi corrupti. "
    "Et eveniet quam non quia quaera"
)

# Subtitle
st.markdown("**Please add your documents using the form:**")

with st.container():

    st.markdown(
        """
        <style>
        .section {
            background-color: #f1ecec;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.form("config_form"):

        filelist = []
        for root, dirs, files in os.walk(txt_pth):
            for file in files:
                filelist.append(file)

        # Create an HTML string for the file list
        current_list = f"[{', '.join(filelist)}]" if filelist else "[]"

        # Combine the section HTML with the dynamically generated file list
        html_content = f"""
        <div class="section">
            <b>Text files</b>
            <p>Current text files: {current_list}</p>
        </div>
        """

        # Render the combined HTML content
        st.markdown(html_content, unsafe_allow_html=True)

        uploaded_text_files = st.file_uploader(
            "Upload text files", accept_multiple_files=True, type="txt"
        )

        submitted = st.form_submit_button("Save")
        if submitted:
            st.success("Form saved successfully!")
import os
from os.path import join, isfile
from utils import load_yaml_file
import streamlit as st

# This function lists files in a directory and provides a delete button for each file.
# If a file is deleted, the page is rerun to refresh the list of files.
# It takes a path to the directory and an optional file extension to filter the files.
def list_files_with_delete(path, extension=None):
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if not extension or f.endswith(extension):
                files.append(join(root, f))

    if not files:
        st.write("No files found.")
        return

    for file_path in files:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(os.path.basename(file_path))
        with col2:
            if st.button(":wastebasket:", key=f"delete_{file_path}"):
                os.remove(file_path)
                st.success(f"Deleted {os.path.basename(file_path)}")
                st.rerun()

# This function saves the configuration for document sources.
# It loads the configuration from a YAML file, creates directories for different file types
def save_config(dataset_path: str):
    config_data = load_yaml_file("config.yaml")

    txt_pth = join(dataset_path, config_data["text_files"])
    html_pth = join(dataset_path, config_data["html_files"])
    pdf_pth = join(dataset_path, config_data["pdf_files"])
    rtdocs_pth = join(dataset_path, config_data["rtdocs_files"])
    yt_pth = join(dataset_path, config_data["yt_video_links"])
    web_pth = join(dataset_path, config_data["web_urls"])

    yt_file = join(yt_pth, "yt_video_links.txt")
    wb_file = join(web_pth, "web_urls.txt")

    yt_content = open(yt_file).read() if isfile(yt_file) else ""
    wb_content = open(wb_file).read() if isfile(wb_file) else ""

    st.header(":page_facing_up: Configure Your Document Sources")

    # File uploaders
    with st.expander(":page_facing_up: Text Files (.txt)"):
        st.write("Uploaded files:")
        list_files_with_delete(txt_pth, ".txt")
        uploaded_txt = st.file_uploader("Upload .txt files", accept_multiple_files=True, type="txt")

    with st.expander(":globe_with_meridians: HTML Files (.html)"):
        st.write("Uploaded files:")
        list_files_with_delete(html_pth, ".html")
        uploaded_html = st.file_uploader("Upload .html files", accept_multiple_files=True, type="html")

    with st.expander(":books: PDF Files (.pdf)"):
        st.write("Uploaded files:")
        list_files_with_delete(pdf_pth, ".pdf")
        uploaded_pdf = st.file_uploader("Upload .pdf files", accept_multiple_files=True, type="pdf")

    with st.expander(":blue_book: ReadTheDocs Files (.html)"):
        st.write("Uploaded files:")
        list_files_with_delete(rtdocs_pth, ".html")
        uploaded_rtdocs = st.file_uploader("Upload ReadTheDocs .html files", accept_multiple_files=True, type="html")

    with st.form(":tv: Links Form"):
        yt_links = st.text_area(":tv: YouTube Video Links", value=yt_content, height=150)
        web_links = st.text_area(":link: Web URLs", value=wb_content, height=150)
        submit = st.form_submit_button(":floppy_disk: Save All")

    if submit:
        # Save link files
        os.makedirs(yt_pth, exist_ok=True)
        os.makedirs(web_pth, exist_ok=True)

        with open(yt_file, "w") as f:
            f.write(yt_links.strip())

        with open(wb_file, "w") as f:
            f.write(web_links.strip())

        # Save uploaded files
        def save_files(uploaded, target_path):
            os.makedirs(target_path, exist_ok=True)
            for file in uploaded:
                with open(join(target_path, file.name), "wb") as f:
                    f.write(file.getbuffer())

        save_files(uploaded_txt, txt_pth)
        save_files(uploaded_html, html_pth)
        save_files(uploaded_pdf, pdf_pth)
        save_files(uploaded_rtdocs, rtdocs_pth)

        st.success(":white_check_mark: Sources saved successfully!")
        st.rerun()

import streamlit as st
import os
import re
from menu import menu_with_redirect
from utils import load_yaml_file_with_db_prompts

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Admin Responses")
st.markdown("View previously asked user questions, AI-generated answers, and source documents.")

def parse_responses_file():
    """Parse the responses.txt file and return a list of question-answer pairs with context"""
    responses_file = "responses.txt"
    if not os.path.exists(responses_file):
        return []
    
    responses = []
    try:
        with open(responses_file, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
            
        for line in lines:
            if line.strip():
                parsed_response = parse_response_line(line)
                if parsed_response:
                    responses.append(parsed_response)
                    
    except Exception as e:
        st.error(f"Error reading responses file: {str(e)}")
        return []
    
    return responses

def parse_response_line(line):
    """Parse a single response line that contains Document objects"""
    try:
        # Extract the input (question)
        input_match = re.search(r"'input': '((?:[^'\\]|\\.)*)'", line)
        question = input_match.group(1) if input_match else "No question found"
        question = question.replace("\\'", "'").replace("\\n", "\n")
        
        # Extract the answer
        answer_match = re.search(r"'answer': '((?:[^'\\]|\\.)*)'(?=\})", line)
        answer = answer_match.group(1) if answer_match else "No answer found"
        answer = answer.replace("\\'", "'").replace("\\n", "\n")
        
        # Extract documents from context
        documents = []
        doc_pattern = r"Document\(id='([^']*)', metadata=\{([^}]*)\}, page_content='((?:[^'\\]|\\.)*)'\)"
        doc_matches = re.findall(doc_pattern, line)
        
        for doc_match in doc_matches:
            doc_id, metadata_str, content = doc_match
            
            # Parse metadata
            metadata = {'id': doc_id}
            metadata_pairs = re.findall(r"'([^']*)': '([^']*)'", metadata_str)
            for key, value in metadata_pairs:
                metadata[key] = value
            
            documents.append({
                'id': doc_id,
                'metadata': metadata,
                'page_content': content.replace("\\'", "'").replace("\\n", "\n")
            })
        
        return {
            'input': question,
            'answer': answer,
            'context': documents
        }
    
    except Exception as e:
        return {
            'input': "Error parsing question",
            'answer': f"Error parsing answer: {str(e)[:100]}",
            'context': []
        }

def display_source_document(doc, index):
    """Display a source document with metadata"""
    st.markdown(f"**:page_facing_up: Document {index + 1}**")
    
    # Display content
    content = doc.get('page_content', '')
    st.markdown("**Content:**")
    st.text(content)
    
    # Display metadata
    st.markdown("**Metadata:**")
    metadata = doc.get('metadata', {})
    
    for key, value in metadata.items():
        st.write(f"- **{key.title()}:** {value}")

# Load and display responses
config_data = load_yaml_file_with_db_prompts("config.yaml")
k_value = config_data.get("nr_retrieved_documents")
print(k_value)

responses = parse_responses_file()

if responses:
    st.markdown(f"### Overview ({len(responses)} responses found)")
    
    # Search functionality
    search_term = st.text_input("Search questions or answers:", placeholder="Enter search term...")
    
    # Filter responses based on search term
    if search_term:
        display_responses = [
            response for response in responses
            if search_term.lower() in response.get('input', '').lower() or
               search_term.lower() in response.get('answer', '').lower()
        ]
        st.success(f"Found {len(display_responses)} matching responses")
    else:
        display_responses = responses
    
    st.markdown("---")
    
    # Display each response
    for i, response in enumerate(reversed(display_responses)):
        question = response.get('input', 'No question found')
        answer = response.get('answer', 'No answer found')
        context = response.get('context', [])
        
        # Display question in an expander
        question_preview = question[:80] + '...' if len(question) > 80 else question
        with st.expander(f"**Q{len(display_responses) - i}:** {question_preview}", expanded=False):
            if len(question) > 80:
                st.markdown(f"**Full Question:** {question}")
            
            st.markdown("**Answer:**")
            st.markdown(answer)
            
            # Display source documents
            if context:
                displayed_docs = context[:k_value] if k_value else context
                st.markdown(f"**Source Documents ({len(displayed_docs)} of {len(context)}):**")
                
                for doc_idx, doc in enumerate(displayed_docs):
                    display_source_document(doc, doc_idx)
                    if doc_idx < len(displayed_docs) - 1:
                        st.markdown("---")
            else:
                st.info("No source documents found.")
else:
    st.info("No responses found. The responses.txt file is empty or doesn't exist.")
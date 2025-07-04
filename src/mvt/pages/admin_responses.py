import streamlit as st
import os
import re
import json
from menu import menu_with_redirect
from utils import load_yaml_file_with_db_prompts
from database import create_connection, get_all_document_response_links, get_documents_for_response, get_response, get_all_responses_with_documents, migrate_text_file_to_database

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# Admin Responses")
st.markdown("View previously asked user questions, AI-generated answers, and source documents.")

def get_responses_from_database():
    """Get responses from database instead of parsing text file"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        responses = []
        db_responses = get_all_responses_with_documents(conn)
        
        for db_response in db_responses:
            # Convert database format to expected format
            context_docs = []
            for doc in db_response.get('documents', []):
                try:
                    metadata_dict = json.loads(doc['metadata']) if doc['metadata'] else {}
                except:
                    metadata_dict = {}
                
                context_docs.append({
                    'id': doc['source'],
                    'metadata': metadata_dict,
                    'page_content': metadata_dict.get('content', 'No content available'),
                    'source': doc['source']
                })
            
            responses.append({
                'input': db_response['question'],
                'answer': db_response['answer'],
                'context': context_docs,
                'created_at': db_response['created_at']
            })
        
        return responses
        
    except Exception as e:
        st.error(f"Error loading responses from database: {e}")
        return []
    finally:
        conn.close()

def get_responses_fallback():
    """Fallback to parse responses from text file if database is empty"""
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
    if not content or content == 'No content available':
        # Try to get content from metadata if not in page_content
        content = doc.get('metadata', {}).get('content', 'No content available')
    
    st.markdown("**Content:**")
    st.text(content)
    
    # Display metadata
    st.markdown("**Metadata:**")
    metadata = doc.get('metadata', {})
    
    # Show source prominently
    source = doc.get('source', metadata.get('source', 'Unknown'))
    st.write(f"- **Source:** {source}")
    
    # Show other metadata excluding content and source
    for key, value in metadata.items():
        if key not in ['content', 'source']:
            st.write(f"- **{key.title()}:** {value}")
    
    # Show database info if available
    if 'id' in doc and doc['id'] != source:
        st.write(f"- **Document ID:** {doc['id']}")

# Load and display responses
config_data = load_yaml_file_with_db_prompts("config.yaml")
k_value = config_data.get("nr_retrieved_documents")
print(k_value)

# Try to get responses from database first, fallback to text file
responses = get_responses_from_database()
if not responses:
    # Try to migrate from text file if database is empty
    conn = create_connection()
    if conn:
        migrated_count = migrate_text_file_to_database(conn)
        conn.close()
        if migrated_count > 0:
            st.success(f"Migrated {migrated_count} responses from text file to database!")
            responses = get_responses_from_database()  # Try again after migration
    
    if not responses:
        st.info("No responses found in database, falling back to text file...")
        responses = get_responses_fallback()

# Add a utility section for admins
if responses and st.session_state.user_type == "admin":
    with st.sidebar:
        st.markdown("### 🛠️ Admin Utilities")
        
        # Check if text file exists and offer migration
        if os.path.exists("responses.txt"):
            st.info("responses.txt file detected")
            if st.button("🔄 Re-run Migration"):
                conn = create_connection()
                if conn:
                    migrated_count = migrate_text_file_to_database(conn)
                    conn.close()
                    if migrated_count > 0:
                        st.success(f"Migrated {migrated_count} additional responses!")
                        st.rerun()
                    else:
                        st.info("No new responses to migrate")
            
            # Option to backup and remove text file after successful migration
            db_responses = get_responses_from_database()
            if db_responses:
                if st.button("🗑️ Archive responses.txt", help="Move responses.txt to responses_backup.txt"):
                    try:
                        import shutil
                        shutil.move("responses.txt", "responses_backup.txt")
                        st.success("Text file archived successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error archiving file: {e}")
        
        # Database stats
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM responses")
                response_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM documents") 
                document_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM docs_response")
                link_count = cur.fetchone()[0]
                
                st.markdown("### 📈 Database Stats")
                st.write(f"Responses: {response_count}")
                st.write(f"Documents: {document_count}")
                st.write(f"Links: {link_count}")
            except Exception as e:
                st.error(f"Error getting stats: {e}")
            finally:
                conn.close()
                
if responses:
    source_info = "📊 **Database**" if get_responses_from_database() else "📄 **Text File**"
    st.markdown(f"### Overview ({len(responses)} responses found) - Source: {source_info}")
    
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
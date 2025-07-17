import streamlit as st
import os
import re
import json
import shutil
from menu import menu_with_redirect
from utils import load_yaml_file_with_db_prompts, escape_markdown
from database import create_connection, get_all_responses_with_documents, migrate_text_file_to_database

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

# Page header
st.markdown("# Admin Responses")
st.markdown("View previously asked user questions, AI-generated answers, and source documents.")

def get_responses_from_database():
    """Get responses from database without caching for latest data"""
    conn = create_connection()
    if not conn:
        return []
    
    try:
        responses = []
        db_responses = get_all_responses_with_documents(conn)
        
        for db_response in db_responses:
            context_docs = []
            for doc in db_response.get('documents', []):
                try:
                    metadata_dict = json.loads(doc['metadata']) if doc['metadata'] else {}
                except:
                    metadata_dict = {}
                
                # Get content from metadata or use source as fallback
                content = metadata_dict.get('content', doc.get('source', 'No content available'))
                
                context_docs.append({
                    'id': doc.get('id'),
                    'metadata': metadata_dict,
                    'page_content': content,
                    'source': metadata_dict.get('source', doc.get('source', 'Unknown'))
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

def get_database_stats():
    """Get current database statistics"""
    conn = create_connection()
    if not conn:
        return None, None, None
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM responses")
        response_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM documents")
        document_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM docs_response")
        link_count = cur.fetchone()[0]
        
        return response_count, document_count, link_count
    except Exception as e:
        st.error(f"Error getting database stats: {e}")
        return None, None, None
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
                'page_content': content.replace("\\'", "'").replace("\\n", "\n"),
                'source': metadata.get('source', doc_id)
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
    """Display a source document with clean formatting"""
    with st.container():
        st.markdown(f"**📄 Document {index + 1}**")
        
        # Source
        source = doc.get('source', 'Unknown')
        st.markdown(f"**Source:** `{source}`")
        
        # Content (truncated for display)
        content = doc.get('page_content', 'No content available')
        if len(content) > 200:
            with st.expander("View content"):
                st.text(content)
        else:
            st.text(content)
        
        # Metadata (excluding content and source)
        metadata = doc.get('metadata', {})
        relevant_metadata = {k: v for k, v in metadata.items() 
                           if k not in ['content', 'source'] and v}
        
        if relevant_metadata:
            st.caption(f"Metadata: {', '.join([f'{k}: {v}' for k, v in relevant_metadata.items()])}")

# Load configuration
config_data = load_yaml_file_with_db_prompts("config.yaml")
k_value = config_data.get("nr_retrieved_documents")

# Sidebar for admin utilities
with st.sidebar:
    st.markdown("### 🛠️ Admin Utilities")
    
    # Add refresh button
    if st.button("🔄 Refresh Data", help="Refresh all data from database"):
        st.rerun()
    
    # Database stats with latest values
    response_count, document_count, link_count = get_database_stats()
    
    if response_count is not None:
        st.metric("Responses", response_count)
        st.metric("Documents", document_count)
        st.metric("Links", link_count)
    else:
        st.error("Unable to fetch database statistics")
    
    # Migration utilities
    if os.path.exists("responses.txt"):
        st.info("📄 responses.txt detected")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Migrate", help="Migrate from text file to database"):
                conn = create_connection()
                if conn:
                    migrated_count = migrate_text_file_to_database(conn)
                    conn.close()
                    if migrated_count > 0:
                        st.success(f"Migrated {migrated_count} responses!")
                        st.rerun()
                    else:
                        st.info("No new responses to migrate")
        
        with col2:
            if st.button("🗑️ Archive", help="Move responses.txt to backup"):
                try:
                    shutil.move("responses.txt", "responses_backup.txt")
                    st.success("Archived successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# Main content
st.markdown("---")

# Always fetch fresh data from database
responses = get_responses_from_database()
if not responses:
    # Try to migrate from text file if database is empty
    conn = create_connection()
    if conn:
        migrated_count = migrate_text_file_to_database(conn)
        conn.close()
        if migrated_count > 0:
            st.success(f"✅ Migrated {migrated_count} responses from text file to database!")
            responses = get_responses_from_database()
    
    if not responses:
        st.info("No responses found in database, checking text file...")
        responses = get_responses_fallback()

if responses:
    # Header with source info and timestamp
    source_info = "Database" if get_responses_from_database() else "Text File"
    current_time = st.empty()
    current_time.markdown(f"### 📊 {len(responses)} Responses (Source: {source_info}) - Last updated: {st.session_state.get('last_update', 'Just now')}")
    
    # Auto-refresh option
    auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=False)
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()

    # Search functionality
    search_term = st.text_input("🔍 Search", placeholder="Search questions or answers...")
    
    # Filter responses
    if search_term:
        display_responses = [
            response for response in responses
            if search_term.lower() in response.get('input', '').lower() or
               search_term.lower() in response.get('answer', '').lower()
        ]
        if display_responses:
            st.success(f"Found {len(display_responses)} matching responses")
        else:
            st.warning("No matching responses found")
    else:
        display_responses = responses
    
    st.markdown("---")
    
    # Display responses
    for i, response in enumerate(display_responses):
        question = response.get('input', 'No question found')
        answer = response.get('answer', 'No answer found')
        context = response.get('context', [])
        created_at = response.get('created_at', '')
        
        # Question preview
        question_preview = question[:80] + '...' if len(question) > 80 else question
        
        with st.expander(f"**❓ Q{len(display_responses) - i}:** {question_preview}", expanded=False):
            # Full question if truncated
            if len(question) > 80:
                st.markdown(f"**Full Question:** {question}")
            
            # Timestamp
            if created_at:
                st.caption(f"Asked: {created_at}")
            
            # Answer
            st.markdown("**🤖 Answer:**")
            st.markdown(escape_markdown(answer))
            
            # Source documents
            if context:
                displayed_docs = context[:k_value] if k_value else context
                st.markdown(f"**📚 Source Documents ({len(displayed_docs)} of {len(context)}):**")
                
                for doc_idx, doc in enumerate(displayed_docs):
                    display_source_document(doc, doc_idx)
                    if doc_idx < len(displayed_docs) - 1:
                        st.markdown("---")
            else:
                st.info("No source documents found.")
else:
    st.info("💡 No responses found. The system is ready to receive questions!")
import sqlite3
import os
import json
import re

# This script creates a SQLite database to store user information.
# It includes functions to create a connection to the database, create a table for users,
# insert a new user, update user information, and retrieve user data.
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    username text NOT NULL UNIQUE,
                    email text NOT NULL UNIQUE,
                    type text DEFAULT 'guest',
                    user_group text,
                    email_verified integer DEFAULT 0
                );'''
        conn.cursor().execute(sql)
    except sqlite3.Error as e:
        print(e)

# This function creates a new user in the database.
# It takes a connection object, username, email, and type as parameters.
def insert_user(conn, username, email, type):
    sql = '''INSERT INTO users(username, email, type) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (username, email, type))
    conn.commit()
    return cur.lastrowid

# This function updates the user type in the database.
# It takes a connection object, email, and type as parameters.
def update_user_loggedin(conn, email, loggedin):
    sql = '''UPDATE users SET loggedin = ? WHERE email = ?'''
    cur = conn.cursor()
    cur.execute(sql, (loggedin, email))
    conn.commit()

# This function updates the user group in the database.
# It takes a connection object, email, and user group as parameters.
def update_user_email_verified(conn, email, email_verified):
    sql = '''UPDATE users SET email_verified = ? WHERE email = ?'''
    cur = conn.cursor()
    cur.execute(sql, (email_verified, email))
    conn.commit()

# This function retrieves user data from the database.
# It takes a connection object and email as parameters.
def get_user(conn, email):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error during user loading data: {e}")
        return None

def create_prompts_table(conn):
    """Create a table to store system and query rewriting prompts"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS prompts (
                    id integer PRIMARY KEY,
                    prompt_type text NOT NULL,
                    prompt_value text NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );'''
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def save_prompt(conn, prompt_type, prompt_value):
    """Save or update a prompt in the database"""
    try:
        # Check if prompt already exists
        cur = conn.cursor()
        cur.execute("SELECT id FROM prompts WHERE prompt_type = ?", (prompt_type,))
        existing = cur.fetchone()
        
        if existing:
            # Update existing prompt
            sql = '''UPDATE prompts SET prompt_value = ?, updated_at = CURRENT_TIMESTAMP 
                     WHERE prompt_type = ?'''
            cur.execute(sql, (prompt_value, prompt_type))
        else:
            # Insert new prompt
            sql = '''INSERT INTO prompts(prompt_type, prompt_value) VALUES(?,?)'''
            cur.execute(sql, (prompt_type, prompt_value))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error saving prompt: {e}")
        return False

def get_prompt(conn, prompt_type):
    """Retrieve a specific prompt from the database"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT prompt_value FROM prompts WHERE prompt_type = ?", (prompt_type,))
        result = cur.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error retrieving prompt: {e}")
        return None

def get_all_prompts(conn):
    """Retrieve all prompts from the database"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT prompt_type, prompt_value, updated_at FROM prompts ORDER BY prompt_type")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving prompts: {e}")
        return []

# ==================== ADDITIONAL FUNCTIONS FOR OTHER TABLES ====================

def create_response_table(conn):
    """Create a table to store responses"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS responses (
                    id integer PRIMARY KEY,
                    answer text NOT NULL,
                    question text NOT NULL,
                    id_user integer,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_user) REFERENCES users (id)
                );'''
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def create_document_table(conn):
    """Create a table to store documents"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS documents (
                    id integer PRIMARY KEY,
                    source text NOT NULL,
                    metadata text,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );'''
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def create_docs_response_table(conn):
    """Create a junction table to link documents and responses"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS docs_response (
                    id integer PRIMARY KEY,
                    id_response integer NOT NULL,
                    id_document integer NOT NULL,
                    date_p TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_response) REFERENCES responses (id),
                    FOREIGN KEY (id_document) REFERENCES documents (id)
                );'''
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Response table functions
def insert_response(conn, answer, question, id_user=None):
    """Insert a new response into the database"""
    try:
        sql = '''INSERT INTO responses(answer, question, id_user) VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (answer, question, id_user))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting response: {e}")
        return None

def get_response(conn, response_id):
    """Retrieve a response by ID"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM responses WHERE id = ?", (response_id,))
        return cur.fetchone()
    except sqlite3.Error as e:
        print(f"Error retrieving response: {e}")
        return None

def get_responses_by_user(conn, user_id):
    """Retrieve all responses for a specific user"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM responses WHERE id_user = ? ORDER BY created_at DESC", (user_id,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving user responses: {e}")
        return []

def update_response(conn, response_id, answer=None, question=None):
    """Update a response"""
    try:
        updates = []
        params = []
        
        if answer is not None:
            updates.append("answer = ?")
            params.append(answer)
        if question is not None:
            updates.append("question = ?")
            params.append(question)
            
        if not updates:
            return False
            
        params.append(response_id)
        sql = f"UPDATE responses SET {', '.join(updates)} WHERE id = ?"
        
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating response: {e}")
        return False

def delete_response(conn, response_id):
    """Delete a response and its associated document links"""
    try:
        cur = conn.cursor()
        # First delete associated docs_response entries
        cur.execute("DELETE FROM docs_response WHERE id_response = ?", (response_id,))
        # Then delete the response
        cur.execute("DELETE FROM responses WHERE id = ?", (response_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting response: {e}")
        return False

# Document table functions
def insert_document(conn, source, metadata=None):
    """Insert a new document into the database"""
    try:
        sql = '''INSERT INTO documents(source, metadata) VALUES(?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (source, metadata))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting document: {e}")
        return None

def get_document(conn, document_id):
    """Retrieve a document by ID"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
        return cur.fetchone()
    except sqlite3.Error as e:
        print(f"Error retrieving document: {e}")
        return None

def get_document_by_source(conn, source):
    """Retrieve a document by source"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM documents WHERE source = ?", (source,))
        return cur.fetchone()
    except sqlite3.Error as e:
        print(f"Error retrieving document by source: {e}")
        return None

def get_all_documents(conn):
    """Retrieve all documents"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM documents ORDER BY created_at DESC")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving documents: {e}")
        return []

def update_document(conn, document_id, source=None, metadata=None):
    """Update a document"""
    try:
        updates = []
        params = []
        
        if source is not None:
            updates.append("source = ?")
            params.append(source)
        if metadata is not None:
            updates.append("metadata = ?")
            params.append(metadata)
            
        if not updates:
            return False
            
        params.append(document_id)
        sql = f"UPDATE documents SET {', '.join(updates)} WHERE id = ?"
        
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating document: {e}")
        return False

def delete_document(conn, document_id):
    """Delete a document and its associated response links"""
    try:
        cur = conn.cursor()
        # First delete associated docs_response entries
        cur.execute("DELETE FROM docs_response WHERE id_document = ?", (document_id,))
        # Then delete the document
        cur.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting document: {e}")
        return False

# docs_response junction table functions
def link_document_response(conn, id_response, id_document):
    """Link a document to a response"""
    try:
        sql = '''INSERT INTO docs_response(id_response, id_document) VALUES(?,?)'''
        cur = conn.cursor()
        cur.execute(sql, (id_response, id_document))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error linking document to response: {e}")
        return None

def get_documents_for_response(conn, response_id):
    """Get all documents linked to a specific response"""
    try:
        cur = conn.cursor()
        sql = '''SELECT d.* FROM documents d
                 JOIN docs_response dr ON d.id = dr.id_document
                 WHERE dr.id_response = ?'''
        cur.execute(sql, (response_id,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving documents for response: {e}")
        return []

def get_responses_for_document(conn, document_id):
    """Get all responses linked to a specific document"""
    try:
        cur = conn.cursor()
        sql = '''SELECT r.* FROM responses r
                 JOIN docs_response dr ON r.id = dr.id_response
                 WHERE dr.id_document = ?'''
        cur.execute(sql, (document_id,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving responses for document: {e}")
        return []

def unlink_document_response(conn, id_response, id_document):
    """Remove the link between a document and response"""
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM docs_response WHERE id_response = ? AND id_document = ?", 
                   (id_response, id_document))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error unlinking document from response: {e}")
        return False

def get_all_document_response_links(conn):
    """Get all document-response links with details"""
    try:
        cur = conn.cursor()
        sql = '''SELECT dr.id, dr.date_p, r.question, r.answer, d.source, d.metadata
                 FROM docs_response dr
                 JOIN responses r ON dr.id_response = r.id
                 JOIN documents d ON dr.id_document = d.id
                 ORDER BY dr.date_p DESC'''
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving document-response links: {e}")
        return []

# Utility function to create all tables
def create_all_tables(conn):
    """Create all tables in the database"""
    create_table(conn)  # users table
    create_prompts_table(conn)
    create_response_table(conn)
    create_document_table(conn)
    create_docs_response_table(conn)

def get_all_responses_with_documents(conn):
    """Get all responses with their associated documents"""
    try:
        cur = conn.cursor()
        sql = '''SELECT r.id, r.question, r.answer, r.created_at, r.id_user,
                        GROUP_CONCAT(d.id || '|||' || d.source || '|||' || COALESCE(d.metadata, '')) as documents
                 FROM responses r
                 LEFT JOIN docs_response dr ON r.id = dr.id_response
                 LEFT JOIN documents d ON dr.id_document = d.id
                 GROUP BY r.id, r.question, r.answer, r.created_at, r.id_user
                 ORDER BY r.created_at DESC'''
        cur.execute(sql)
        results = cur.fetchall()
        
        # Process results to separate documents
        processed_results = []
        for row in results:
            response_id, question, answer, created_at, id_user, documents_str = row
            documents = []
            
            if documents_str:
                doc_parts = documents_str.split(',')
                for doc_part in doc_parts:
                    if '|||' in doc_part:
                        parts = doc_part.split('|||')
                        if len(parts) >= 3:
                            doc_id, source, metadata = parts[0], parts[1], parts[2]
                            documents.append({
                                'id': doc_id,
                                'source': source,
                                'metadata': metadata
                            })
            
            processed_results.append({
                'id': response_id,
                'question': question,
                'answer': answer,
                'created_at': created_at,
                'id_user': id_user,
                'documents': documents
            })
        
        return processed_results
    except sqlite3.Error as e:
        print(f"Error retrieving responses with documents: {e}")
        return []

def migrate_text_file_to_database(conn, responses_file="responses.txt"):
    """Migrate existing responses.txt data to database"""
    if not os.path.exists(responses_file):
        return 0
    
    migrated_count = 0
    try:
        with open(responses_file, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
        
        for line in lines:
            if line.strip():
                try:
                    # Parse the response line (similar to admin_responses.py logic)
                    # Extract the input (question)
                    input_match = re.search(r"'input': '((?:[^'\\]|\\.)*)'", line)
                    question = input_match.group(1) if input_match else "Migrated question"
                    question = question.replace("\\'", "'").replace("\\n", "\n")
                    
                    # Extract the answer
                    answer_match = re.search(r"'answer': '((?:[^'\\]|\\.)*)'(?=\})", line)
                    answer = answer_match.group(1) if answer_match else "Migrated answer"
                    answer = answer.replace("\\'", "'").replace("\\n", "\n")
                    
                    # Check if this response already exists to avoid duplicates
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM responses WHERE question = ? AND answer = ? LIMIT 1", (question, answer))
                    if cur.fetchone():
                        continue  # Skip if already exists
                    
                    # Insert response
                    response_id = insert_response(conn, answer, question, None)
                    
                    if response_id:
                        # Extract and process documents
                        doc_pattern = r"Document\(id='([^']*)', metadata=\{([^}]*)\}, page_content='((?:[^'\\]|\\.)*)'\)"
                        doc_matches = re.findall(doc_pattern, line)
                        
                        for doc_match in doc_matches:
                            doc_id, metadata_str, content = doc_match
                            
                            # Parse metadata
                            metadata = {'id': doc_id}
                            metadata_pairs = re.findall(r"'([^']*)': '([^']*)'", metadata_str)
                            for key, value in metadata_pairs:
                                metadata[key] = value
                            metadata['content'] = content.replace("\\'", "'").replace("\\n", "\n")
                            
                            source = metadata.get('source', doc_id)
                            
                            # Check if document exists
                            existing_doc = get_document_by_source(conn, source)
                            if existing_doc:
                                db_doc_id = existing_doc[0]
                            else:
                                # Insert new document
                                metadata_json = json.dumps(metadata)
                                db_doc_id = insert_document(conn, source, metadata_json)
                            
                            # Link document to response
                            if db_doc_id:
                                link_document_response(conn, response_id, db_doc_id)
                        
                        migrated_count += 1
                
                except Exception as e:
                    print(f"Error migrating line: {e}")
                    continue
    
    except Exception as e:
        print(f"Error reading migration file: {e}")
    
    return migrated_count

if __name__ == "__main__":
    conn = create_connection()
    insert_user(conn,"dev","dev@example.com","admin")
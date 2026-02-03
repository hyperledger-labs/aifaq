import streamlit as st
from snowflake.snowpark.context import get_active_session
import uuid
import pandas as pd
import re

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    layout="wide",
    page_title="AIFAQ Pro",
    page_icon="🏢",
    initial_sidebar_state="expanded",
)

# ==========================================
# ENHANCED UI STYLING (IMPROVED FOR ADMIN)
# ==========================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre {
        font-family: 'Fira Code', monospace !important;
    }
    
    /* Dark Theme Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    /* Header */
    header[data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-bottom: 1px solid #334155;
        backdrop-filter: blur(10px);
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    /* Logo */
    .logo-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 12px 24px;
    }
    
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .logo-name {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
    }
    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: 1px solid #334155;
        color: #cbd5e1;
        text-align: left;
        font-weight: 500;
        border-radius: 8px;
        padding: 12px 14px;
        transition: all 0.2s ease;
        width: 100%;
        font-size: 14px;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #334155;
        border-color: #475569;
        color: #f8fafc;
        transform: translateY(-1px);
    }
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    /* Danger Button */
    .danger-btn > button {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        border: none !important;
        color: white !important;
    }
    
    .danger-btn > button:hover {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    }
    /* Chat Input */
    .stChatInput > div {
        background: transparent !important;
    }
    
    .stChatInput textarea {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 15px !important;
        padding: 16px 20px !important;
        transition: all 0.2s ease;
    }
    
    .stChatInput textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        transform: scale(1.05);
    }
    /* === MESSAGE STYLES === */
    .message-container {
        margin-bottom: 24px;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-msg {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 16px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        word-wrap: break-word;
    }
    
    .ai-msg {
        background: #1e293b;
        border: 1px solid #334155;
        color: #e2e8f0;
        padding: 0;
        border-radius: 12px;
        margin: 8px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    
    .ai-msg-content {
        padding: 20px 24px;
        font-size: 15px;
        line-height: 1.7;
    }
    
    .ai-msg-content > *:first-child {
        margin-top: 0;
    }
    
    .ai-msg-content > *:last-child {
        margin-bottom: 0;
    }
    
    .ai-msg p {
        margin: 0 0 12px 0;
    }
    
    .ai-msg p:last-child {
        margin-bottom: 0;
    }
    
    .ai-msg strong {
        color: #f8fafc;
        font-weight: 600;
    }
    
    .ai-msg ul, .ai-msg ol {
        margin: 12px 0;
        padding-left: 24px;
    }
    
    .ai-msg li {
        margin: 8px 0;
        line-height: 1.6;
    }
    
    .ai-msg code {
        background: #334155;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 13px;
        color: #7dd3fc;
        border: 1px solid #475569;
    }
    
    .ai-msg pre {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        overflow-x: auto;
        margin: 16px 0;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .ai-msg pre code {
        background: transparent;
        padding: 0;
        color: #e2e8f0;
        border: none;
    }
    
    .ai-msg h1, .ai-msg h2, .ai-msg h3 {
        color: #f8fafc;
        margin: 20px 0 12px 0;
        font-weight: 600;
        padding-bottom: 8px;
        border-bottom: 1px solid #334155;
    }
    
    .ai-msg h1 { font-size: 22px; }
    .ai-msg h2 { font-size: 19px; }
    .ai-msg h3 { font-size: 17px; }
    
    .ai-msg blockquote {
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        margin: 16px 0;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 0 8px 8px 0;
        color: #cbd5e1;
        font-style: italic;
    }
    
    .ai-msg a {
        color: #60a5fa;
        text-decoration: none;
        border-bottom: 1px dotted #60a5fa;
    }
    
    .ai-msg a:hover {
        color: #93c5fd;
        border-bottom: 1px solid #93c5fd;
    }
    
    .ai-msg table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .ai-msg th, .ai-msg td {
        border: 1px solid #334155;
        padding: 12px 16px;
        text-align: left;
    }
    
    .ai-msg th {
        background: #334155;
        font-weight: 600;
        color: #f8fafc;
    }
    
    .ai-msg tr:nth-child(even) {
        background: rgba(51, 65, 85, 0.3);
    }
    /* Thinking Section */
    .thinking-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px dashed #7c3aed;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        color: #a78bfa;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .thinking-label {
        font-size: 11px;
        font-weight: 700;
        color: #8b5cf6;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    /* Sources */
    .sources-box {
        margin-top: 16px;
        padding: 16px 24px;
        border-top: 1px solid #334155;
        background: rgba(20, 83, 45, 0.2);
    }
    
    .sources-label {
        font-size: 12px;
        font-weight: 600;
        color: #4ade80;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .source-tag {
        display: inline-block;
        background: linear-gradient(135deg, #14532d, #166534);
        border: 1px solid #22c55e;
        color: #4ade80;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }
    
    .source-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    /* Mode Selector */
    .mode-row {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }
    
    .mode-btn {
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid;
    }
    
    .mode-quick {
        background: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.3);
        color: #22c55e;
    }
    
    .mode-quick.active {
        background: rgba(34, 197, 94, 0.2);
        border-color: #22c55e;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
    }
    
    .mode-deep {
        background: rgba(168, 85, 247, 0.1);
        border-color: rgba(168, 85, 247, 0.3);
        color: #a855f7;
    }
    
    .mode-deep.active {
        background: rgba(168, 85, 247, 0.2);
        border-color: #a855f7;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
    }
    /* Badges */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .badge-admin {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #000;
    }
    
    .badge-user {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: #fff;
    }
    /* Section Header */
    .section-title {
        font-size: 11px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 20px 0 10px 0;
    }
    /* Page Header */
    .page-title {
        font-size: 28px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #334155;
        background: linear-gradient(135deg, #f8fafc, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    /* Cards (Enhanced for Admin) */
    .card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        margin-bottom: 20px;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .admin-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #334155;
    }
    
    .admin-card-header h3 {
        margin: 0;
        color: #f8fafc;
        font-size: 18px;
        font-weight: 600;
    }
    /* Form Inputs */
    .stTextInput input,
    .stSelectbox > div > div {
        background: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        color: #f8fafc !important;
        transition: all 0.2s ease;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    /* Hide defaults */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 100px !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .user-msg { max-width: 90%; }
    }
    /* Simplified Multi-Select (Enhanced) */
    .select-all-row {
        background: #334155;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .item-row {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .item-row:hover {
        background: #334155;
        border-color: #475569;
    }
    
    .item-row.selected {
        background: rgba(59, 130, 246, 0.1);
        border-color: #3b82f6;
    }
    
    .item-checkbox {
        margin-right: 16px;
    }
    
    .item-content {
        flex-grow: 1;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        align-items: center;
    }
    
    .bulk-action-bar {
        background: linear-gradient(135deg, #1e3a8a, #1e40af);
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        position: sticky;
        top: 0;
        z-index: 10;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Admin Icons */
    .admin-icon {
        font-size: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# CONSTANTS
# ==========================================
DB_NAME = "VERSION2_DB"
SCHEMA_NAME = "APP_SCHEMA"
MODEL_SMALL = "mistral-7b"
MODEL_LARGE = "mixtral-8x7b"
EMBED_MODEL = "snowflake-arctic-embed-m"  #  SINGLE SOURCE OF TRUTH

# ==========================================
# ENHANCED CONSTANTS & CONFIGS
# ==========================================
RAG_CONFIG = {
    "max_chunks": 6,
    "similarity_threshold": 0.15,
    "rerank_candidates": 25,
    "max_chunk_text": 700,
    "chunk_overlap": 100,
    "line_numbers": True,
}

# Financial-specific RAG config
FINANCIAL_RAG_CONFIG = {
    "max_chunks": 10,  # More chunks for financial docs
    "similarity_threshold": 0.12,  # Lower threshold for number matching
    "rerank_candidates": 40,
    "max_chunk_text": 500,  # Smaller chunks for precise numbers
    "chunk_overlap": 150,
    "line_numbers": True,
    "number_boost_factor": 1.5,
    "financial_keywords": [
        "revenue",
        "profit",
        "loss",
        "income",
        "expense",
        "cost",
        "margin",
        "balance",
        "sheet",
        "cash",
        "flow",
        "statement",
        "equity",
        "asset",
        "liability",
        "ebitda",
        "eps",
        "dividend",
        "tax",
        "depreciation",
        "quarter",
        "q1",
        "q2",
        "q3",
        "q4",
        "annual",
        "fiscal",
        "guidance",
        "million",
        "billion",
        "percentage",
        "growth",
        "decline",
        "increase",
        "decrease",
        "yoy",
        "year",
        "over",
        "year",
        "quarter",
        "qtr",
    ],
}


# ==========================================
# DATABASE SESSION
# ==========================================
@st.cache_resource
def get_db_session():
    return get_active_session()


session = get_db_session()


@st.cache_resource
def init_schema():
    tables = [
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS (USERNAME VARCHAR, TEAM_NAME VARCHAR, UPDATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING (ROLE_NAME VARCHAR, ALLOWED_CATEGORY VARCHAR, CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS (USERNAME VARCHAR PRIMARY KEY, GRANTED_BY VARCHAR, GRANTED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.TEAMS (TEAM_NAME VARCHAR PRIMARY KEY, DESCRIPTION VARCHAR, CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.CHAT_SESSIONS (SESSION_ID VARCHAR PRIMARY KEY, USERNAME VARCHAR, TITLE VARCHAR, CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(), UPDATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.CHAT_MESSAGES (MESSAGE_ID VARCHAR PRIMARY KEY, SESSION_ID VARCHAR, ROLE VARCHAR, CONTENT VARCHAR, SOURCES VARCHAR, CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS (DOC_ID VARCHAR PRIMARY KEY, FILENAME VARCHAR, CATEGORY VARCHAR, UPLOADED_BY VARCHAR, UPLOAD_TS TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.CHUNKS (CHUNK_ID VARCHAR PRIMARY KEY, DOC_ID VARCHAR, CHUNK_TEXT VARCHAR, CHUNK_VEC VECTOR(FLOAT, 768))",
        f"CREATE TABLE IF NOT EXISTS {DB_NAME}.{SCHEMA_NAME}.APP_CATEGORIES (CATEGORY_NAME VARCHAR PRIMARY KEY, DESCRIPTION VARCHAR, CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP())",
    ]
    for t in tables:
        try:
            session.sql(t).collect()
        except:
            pass
    return True


init_schema()


# ==========================================
# HELPERS
# ==========================================
def esc(t):
    if t is None:
        return ""
    return str(t).replace("'", "''")


def qry(sql, default=None):
    try:
        result = session.sql(sql).collect()
        return result if result is not None else default
    except Exception as e:
        print(f"Query error: {e}")
        return default


def val(sql, default=None):
    try:
        r = qry(sql, None)
        if r is None or not isinstance(r, (list, tuple)) or len(r) == 0:
            return default
        first_row = r[0]
        if first_row is None:
            return default
        if hasattr(first_row, "__getitem__"):
            try:
                value = first_row[0]
                return value if value is not None else default
            except:
                return default
        return default
    except Exception as e:
        print(f"Value error: {e}")
        return default


def df_page(sql, pg=0, sz=50):
    try:
        return session.sql(f"{sql} LIMIT {sz} OFFSET {pg*sz}").to_pandas()
    except Exception as e:
        print(f"Dataframe error: {e}")
        return None


# ==========================================
# USER FUNCTIONS
# ==========================================
def get_current_user():
    r = val("SELECT CURRENT_USER()", "UNKNOWN")
    return str(r).replace('"', "").upper() if r else "UNKNOWN"


def check_is_admin(username):
    if not username:
        return False
    result = qry(
        f"SELECT 1 FROM {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS WHERE UPPER(USERNAME)='{esc(username.upper())}'"
    )
    if result and len(result) > 0:
        return True
    admin_count = val(f"SELECT COUNT(*) FROM {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS", 0)
    if not admin_count or admin_count == 0:
        try:
            session.sql(
                f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS (USERNAME, GRANTED_BY) VALUES ('{esc(username.upper())}', 'SYSTEM_AUTO')"
            ).collect()
            return True
        except:
            return False
    return False


@st.cache_data(ttl=60)
def get_team(_u):
    if not _u:
        return "GUEST"
    r = val(
        f"SELECT TEAM_NAME FROM {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS WHERE UPPER(USERNAME)='{esc(_u.upper())}' ORDER BY UPDATED_AT DESC LIMIT 1"
    )
    return str(r).upper() if r else "GUEST"


@st.cache_data(ttl=60)
def get_access(_t, _a):
    if _a:
        return "ALL"
    if not _t or _t == "GUEST":
        return "NONE"
    result = val(
        f"SELECT LISTAGG(DISTINCT ALLOWED_CATEGORY, ', ') FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)='{esc(_t.upper())}'"
    )
    return result if result else "NONE"


# ==========================================
# CATEGORY FUNCTIONS
# ==========================================
def get_all_categories():
    sql = f"SELECT DISTINCT CATEGORY_NAME FROM {DB_NAME}.{SCHEMA_NAME}.APP_CATEGORIES ORDER BY CATEGORY_NAME"
    r = qry(sql, [])
    if not r or not isinstance(r, list):
        return []
    categories = []
    for row in r:
        if row:
            try:
                cat_name = row[0]
                if cat_name:
                    categories.append(str(cat_name))
            except:
                continue
    return sorted(categories)


def create_category_db(name):
    if not name:
        return False, "Category name is required"
    try:
        session.sql(
            f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.APP_CATEGORIES (CATEGORY_NAME) VALUES ('{esc(name.upper())}')"
        ).collect()
        return True, f"Category '{name}' added"
    except Exception as e:
        return False, str(e)


def delete_category_db(name):
    if not name:
        return False, "Category name is required"
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.APP_CATEGORIES WHERE UPPER(CATEGORY_NAME)='{esc(name.upper())}'"
        ).collect()
        return True, f"Category '{name}' deleted"
    except Exception as e:
        return False, str(e)


# ==========================================
# TEAM FUNCTIONS
# ==========================================
@st.cache_data(ttl=120)
def get_teams():
    sql = f"SELECT DISTINCT TEAM_NAME FROM (SELECT TEAM_NAME FROM {DB_NAME}.{SCHEMA_NAME}.TEAMS UNION SELECT TEAM_NAME FROM {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS WHERE TEAM_NAME!='GUEST' UNION SELECT ROLE_NAME FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING) WHERE TEAM_NAME!='SUPER_ADMIN' AND TEAM_NAME IS NOT NULL"
    r = qry(sql, [])
    if not r or not isinstance(r, list):
        return []
    teams = []
    for row in r:
        if row:
            try:
                team_name = row[0]
                if team_name:
                    teams.append(str(team_name))
            except:
                continue
    return sorted(teams)


@st.cache_data(ttl=30)
def get_categories(_t):
    if not _t:
        return []
    sql = f"SELECT ALLOWED_CATEGORY FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)='{esc(_t.upper())}'"
    r = qry(sql, [])
    if not r or not isinstance(r, list):
        return []
    categories = []
    for row in r:
        if row:
            try:
                cat = row[0]
                if cat:
                    categories.append(str(cat))
            except:
                continue
    return categories


# ==========================================
# DATA LOADERS
# ==========================================
def load_users(pg=0, sz=50):
    sql = f"SELECT u.USERNAME, COALESCE(u.TEAM_NAME,'GUEST') as TEAM, CASE WHEN a.USERNAME IS NOT NULL THEN '✓' ELSE '' END as ADMIN, u.UPDATED_AT FROM {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS u LEFT JOIN {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS a ON UPPER(u.USERNAME)=UPPER(a.USERNAME) ORDER BY u.USERNAME"
    return df_page(sql, pg, sz)


def load_admins():
    try:
        return session.sql(
            f"SELECT USERNAME, GRANTED_BY, GRANTED_AT FROM {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS ORDER BY USERNAME"
        ).to_pandas()
    except:
        return pd.DataFrame(columns=["USERNAME", "GRANTED_BY", "GRANTED_AT"])


def load_rules(pg=0, sz=50):
    sql = f"SELECT ROLE_NAME as TEAM, ALLOWED_CATEGORY as CATEGORY, CREATED_AT FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING ORDER BY ROLE_NAME, ALLOWED_CATEGORY"
    return df_page(sql, pg, sz)


def load_docs(pg=0, sz=50):
    sql = f"SELECT DOC_ID, FILENAME, CATEGORY, UPLOADED_BY, UPLOAD_TS FROM {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS ORDER BY UPLOAD_TS DESC"
    return df_page(sql, pg, sz)


def load_members(team, pg=0, sz=50):
    if not team:
        return None
    sql = f"SELECT u.USERNAME, CASE WHEN a.USERNAME IS NOT NULL THEN '✓' ELSE '' END as ADMIN, u.UPDATED_AT as JOINED FROM {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS u LEFT JOIN {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS a ON UPPER(u.USERNAME)=UPPER(a.USERNAME) WHERE UPPER(u.TEAM_NAME)='{esc(team.upper())}' ORDER BY u.USERNAME"
    return df_page(sql, pg, sz)


def count_tbl(tbl):
    result = val(f"SELECT COUNT(*) FROM {DB_NAME}.{SCHEMA_NAME}.{tbl}", 0)
    return result if result is not None else 0


# ==========================================
# USER MANAGEMENT
# ==========================================
def create_user(username, password, team=None):
    if not username:
        return False, "Username is required"
    u = "".join(c for c in username if c.isalnum() or c == "_").upper()
    if not u or len(password) < 6:
        return False, "Invalid username or password < 6 chars"
    try:
        session.sql("CREATE ROLE IF NOT EXISTS AIFAQ_VIEWER_ROLE").collect()
        session.sql(
            f"CREATE USER IF NOT EXISTS {u} PASSWORD='{esc(password)}' DEFAULT_ROLE=AIFAQ_VIEWER_ROLE MUST_CHANGE_PASSWORD=FALSE"
        ).collect()
        session.sql(f"GRANT ROLE AIFAQ_VIEWER_ROLE TO USER {u}").collect()
        if team and team not in ("SUPER_ADMIN", "GUEST", ""):
            assign_team(u, team)
        get_teams.clear()
        return True, f"User '{u}' created"
    except Exception as e:
        return False, str(e)


# ==========================================
# PASSWORD RESET FUNCTION
# ==========================================
def reset_user_password(username, new_password):
    """Reset password for existing user"""
    if not username or len(new_password) < 6:
        return False, "Invalid username or password < 6 chars"
    try:
        # Use Snowflake's ALTER USER command
        session.sql(
            f"ALTER USER {username} SET PASSWORD = '{esc(new_password)}'"
        ).collect()
        return True, f"Password reset for user '{username}'"
    except Exception as e:
        return False, str(e)


def assign_team(username, team):
    if not username or not team:
        return False, "Username and team are required"
    try:
        sql = f"MERGE INTO {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS t USING (SELECT '{esc(username.upper())}' as U, '{esc(team.upper())}' as T) s ON UPPER(t.USERNAME)=s.U WHEN MATCHED THEN UPDATE SET TEAM_NAME=s.T, UPDATED_AT=CURRENT_TIMESTAMP() WHEN NOT MATCHED THEN INSERT (USERNAME, TEAM_NAME) VALUES (s.U, s.T)"
        session.sql(sql).collect()
        get_team.clear()
        return True, f"Assigned '{username}' → '{team}'"
    except Exception as e:
        return False, str(e)


def bulk_assign(users, team):
    if not users or not team:
        return 0
    vals = ", ".join(
        [f"('{esc(u.upper())}', '{esc(team.upper())}')" for u in users if u]
    )
    if not vals:
        return 0
    try:
        sql = f"MERGE INTO {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS t USING (SELECT column1 as U, column2 as T FROM VALUES {vals}) s ON UPPER(t.USERNAME)=s.U WHEN MATCHED THEN UPDATE SET TEAM_NAME=s.T, UPDATED_AT=CURRENT_TIMESTAMP() WHEN NOT MATCHED THEN INSERT (USERNAME, TEAM_NAME) VALUES (s.U, s.T)"
        session.sql(sql).collect()
        get_team.clear()
        return len(users)
    except Exception as e:
        print(f"Bulk assign error: {e}")
        return 0


def bulk_delete(users, sf=False):
    if not users:
        return 0
    lst = ", ".join([f"'{esc(u.upper())}'" for u in users if u])
    if not lst:
        return 0
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS WHERE UPPER(USERNAME) IN ({lst})"
        ).collect()
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS WHERE UPPER(USERNAME) IN ({lst})"
        ).collect()
        if sf:
            for u in users:
                if u:
                    session.sql(f"DROP USER IF EXISTS {u}").collect()
        get_team.clear()
        return len(users)
    except Exception as e:
        print(f"Bulk delete error: {e}")
        return 0


def create_team_db(name, desc=""):
    if not name:
        return False, "Team name is required"
    try:
        session.sql(
            f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.TEAMS (TEAM_NAME, DESCRIPTION) VALUES ('{esc(name.upper())}', '{esc(desc)}')"
        ).collect()
        get_teams.clear()
        return True, f"Team '{name}' created"
    except Exception as e:
        return False, str(e)


def delete_team_db(name):
    if not name:
        return False, "Team name is required"
    n = esc(name.upper())
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.TEAMS WHERE UPPER(TEAM_NAME)='{n}'"
        ).collect()
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)='{n}'"
        ).collect()
        session.sql(
            f"UPDATE {DB_NAME}.{SCHEMA_NAME}.APP_USER_TEAMS SET TEAM_NAME='GUEST' WHERE UPPER(TEAM_NAME)='{n}'"
        ).collect()
        get_teams.clear()
        get_team.clear()
        return True, f"Team '{name}' deleted"
    except Exception as e:
        return False, str(e)


def add_admin_db(username, by):
    if not username:
        return False, "Username is required"
    try:
        session.sql(
            f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS (USERNAME, GRANTED_BY) VALUES ('{esc(username.upper())}', '{esc(by.upper() if by else 'SYSTEM')}')"
        ).collect()
        return True, f"'{username}' is now admin"
    except Exception as e:
        return False, str(e)


def remove_admin_db(username, curr):
    if not username:
        return False, "Username is required"
    if curr and username.upper() == curr.upper():
        return False, "Cannot remove yourself"
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.ADMIN_USERS WHERE UPPER(USERNAME)='{esc(username.upper())}'"
        ).collect()
        return True, f"Removed admin: '{username}'"
    except Exception as e:
        return False, str(e)


def grant_cat(team, cat):
    if not team or not cat:
        return False, "Team and category are required"
    try:
        sql = f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING (ROLE_NAME, ALLOWED_CATEGORY) SELECT '{esc(team.upper())}', '{esc(cat.upper())}' WHERE NOT EXISTS (SELECT 1 FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)='{esc(team.upper())}' AND UPPER(ALLOWED_CATEGORY)='{esc(cat.upper())}')"
        session.sql(sql).collect()
        get_access.clear()
        return True, f"Granted '{cat}' → '{team}'"
    except Exception as e:
        return False, str(e)


def revoke_cat(team, cat):
    if not team or not cat:
        return False, "Team and category are required"
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)='{esc(team.upper())}' AND UPPER(ALLOWED_CATEGORY)='{esc(cat.upper())}'"
        ).collect()
        get_access.clear()
        return True, "Revoked"
    except Exception as e:
        return False, str(e)


def bulk_grant(team, cats):
    if not cats or not team:
        return 0
    vals = ", ".join(
        [f"('{esc(team.upper())}', '{esc(c.upper())}')" for c in cats if c]
    )
    if not vals:
        return 0
    try:
        sql = f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING (ROLE_NAME, ALLOWED_CATEGORY) SELECT column1, column2 FROM VALUES {vals} WHERE NOT EXISTS (SELECT 1 FROM {DB_NAME}.{SCHEMA_NAME}.ROLE_ACCESS_MAPPING WHERE UPPER(ROLE_NAME)=column1 AND UPPER(ALLOWED_CATEGORY)=column2)"
        session.sql(sql).collect()
        get_access.clear()
        return len(cats)
    except Exception as e:
        print(f"Bulk grant error: {e}")
        return 0


def bulk_revoke(rules):
    """rules: list of tuples (team, category)"""
    if not rules:
        return 0
    try:
        for team, category in rules:
            revoke_cat(team, category)
        return len(rules)
    except Exception as e:
        print(f"Bulk revoke error: {e}")
        return 0


# ==========================================
# ENHANCED DOCUMENT INGESTION
# ==========================================
def ingest_doc(file, cat):
    """Enhanced ingestion with line numbers and financial-aware chunking"""
    if not file or not cat:
        return False, "File and category are required"

    try:
        name = "".join(c for c in file.name if c.isalnum() or c in "._-")
        doc_id = str(uuid.uuid4())

        # Upload to stage
        session.file.put_stream(
            file,
            f"@{DB_NAME}.{SCHEMA_NAME}.DOC_STAGE/{name}",
            auto_compress=False,
            overwrite=True,
        )

        # Parse document
        parse_sql = f"""
            SELECT SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
                '@{DB_NAME}.{SCHEMA_NAME}.DOC_STAGE', 
                '{name}'
            ):content::STRING as content
        """
        content_result = session.sql(parse_sql).collect()

        if not content_result or len(content_result) == 0:
            return False, "Failed to parse document"

        full_content = content_result[0]["CONTENT"]

        # Enhanced chunking with line numbers
        chunks = create_enhanced_chunks(full_content, doc_id, cat)

        # Insert document record
        session.sql(
            f"""
            INSERT INTO {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS 
            (DOC_ID, FILENAME, CATEGORY, UPLOADED_BY) 
            VALUES ('{doc_id}', '{esc(name)}', '{esc(cat.upper())}', CURRENT_USER())
        """
        ).collect()

        return True, f"Document indexed with {len(chunks)} chunks"

    except Exception as e:
        return False, str(e)


def create_enhanced_chunks(content, doc_id, category):
    """Create enhanced chunks with line numbers and financial document awareness"""
    if not content:
        return []

    lines = content.split("\n")
    chunks = []
    chunk_id = 0

    # Determine if this is a financial document
    is_financial = is_financial_document(content, category)
    config = FINANCIAL_RAG_CONFIG if is_financial else RAG_CONFIG

    # Enhanced chunking strategy
    if is_financial:
        # For financial docs, preserve table structures and statements
        chunks = chunk_financial_document(lines, doc_id, config)
    else:
        # Standard chunking with line numbers
        chunks = chunk_standard_document(lines, doc_id, config)

    return chunks


def is_financial_document(content, category):
    """Detect if document contains financial content"""
    content_lower = content.lower()
    category_lower = category.lower()

    # Check category first
    if any(
        kw in category_lower
        for kw in ["finance", "financial", "accounting", "audit", "fiscal"]
    ):
        return True

    # Check content for financial keywords
    financial_keywords = FINANCIAL_RAG_CONFIG["financial_keywords"]
    keyword_count = sum(1 for kw in financial_keywords if kw in content_lower)

    # If more than 5 financial keywords, treat as financial doc
    return keyword_count > 5


def chunk_financial_document(lines, doc_id, config):
    """Special chunking for financial documents"""
    chunks = []
    current_chunk = []
    current_lines = []
    chunk_size = 0
    chunk_id = 0

    for idx, line in enumerate(lines, 1):
        line_len = len(line)

        # Add line with number prefix
        numbered_line = f"[L{idx:04d}] {line}"
        current_chunk.append(numbered_line)
        current_lines.append(idx)
        chunk_size += line_len

        # Check if we should chunk here (financial statement boundaries)
        if should_chunk_financial_line(line, chunk_size, config["max_chunk_text"]):
            if current_chunk:
                chunk_text = "\n".join(current_chunk)
                # Add metadata about line range
                chunk_text = f"=== LINES {current_lines[0]}-{current_lines[-1]} ===\n{chunk_text}"

                create_chunk_record(doc_id, chunk_text, chunk_id)
                chunks.append(chunk_text)

                # Reset with overlap
                overlap_start = max(
                    0, len(current_chunk) - config["chunk_overlap"] // 50
                )
                current_chunk = current_chunk[overlap_start:]
                current_lines = current_lines[overlap_start:]
                chunk_size = sum(len(l) for l in current_chunk)
                chunk_id += 1

    # Add remaining chunk
    if current_chunk:
        chunk_text = "\n".join(current_chunk)
        chunk_text = (
            f"=== LINES {current_lines[0]}-{current_lines[-1]} ===\n{chunk_text}"
        )
        create_chunk_record(doc_id, chunk_text, chunk_id)
        chunks.append(chunk_text)

    return chunks


def chunk_standard_document(lines, doc_id, config):
    """Standard chunking with line numbers"""
    chunks = []
    current_chunk = []
    current_lines = []
    chunk_size = 0
    chunk_id = 0

    for idx, line in enumerate(lines, 1):
        line_len = len(line)

        # Add line with number prefix
        numbered_line = f"[L{idx:04d}] {line}"
        current_chunk.append(numbered_line)
        current_lines.append(idx)
        chunk_size += line_len

        # Simple size-based chunking
        if chunk_size >= config["max_chunk_text"]:
            if current_chunk:
                chunk_text = "\n".join(current_chunk)
                chunk_text = f"=== LINES {current_lines[0]}-{current_lines[-1]} ===\n{chunk_text}"

                create_chunk_record(doc_id, chunk_text, chunk_id)
                chunks.append(chunk_text)

                # Reset with overlap
                overlap_start = max(
                    0, len(current_chunk) - config["chunk_overlap"] // 50
                )
                current_chunk = current_chunk[overlap_start:]
                current_lines = current_lines[overlap_start:]
                chunk_size = sum(len(l) for l in current_chunk)
                chunk_id += 1

    # Add remaining chunk
    if current_chunk:
        chunk_text = "\n".join(current_chunk)
        chunk_text = (
            f"=== LINES {current_lines[0]}-{current_lines[-1]} ===\n{chunk_text}"
        )
        create_chunk_record(doc_id, chunk_text, chunk_id)
        chunks.append(chunk_text)

    return chunks


def should_chunk_financial_line(line, current_size, max_size):
    """Determine if we should chunk at this line (financial doc logic)"""
    if current_size >= max_size:
        return True

    line_upper = line.strip().upper()

    # Chunk at financial statement boundaries
    if any(
        boundary in line_upper
        for boundary in [
            "BALANCE SHEET",
            "INCOME STATEMENT",
            "CASH FLOW",
            "STATEMENT OF",
            "QUARTER ENDED",
            "YEAR ENDED",
            "ASSETS",
            "LIABILITIES",
            "EQUITY",
            "REVENUE",
        ]
    ):
        return True

    # Chunk at empty lines after tables
    if line.strip() == "" and current_size > max_size * 0.7:
        return True

    return False


def create_chunk_record(doc_id, chunk_text, chunk_id):
    """✅ FIXED: Insert chunk into database using SELECT (not VALUES) with single EMBED_MODEL"""
    chunk_uuid = str(uuid.uuid4())

    # ✅ Use global EMBED_MODEL constant and SELECT syntax to fix SQL compilation error
    session.sql(
        f"""
        INSERT INTO {DB_NAME}.{SCHEMA_NAME}.CHUNKS 
        (CHUNK_ID, DOC_ID, CHUNK_TEXT, CHUNK_VEC)
        SELECT 
            '{chunk_uuid}',
            '{doc_id}',
            '{esc(chunk_text)}',
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('{EMBED_MODEL}', '{esc(chunk_text)}')
    """
    ).collect()

    return chunk_uuid


def delete_docs(ids):
    if not ids:
        return 0
    lst = ", ".join([f"'{esc(d)}'" for d in ids if d])
    if not lst:
        return 0
    try:
        # Delete from chunks first (foreign key relationship)
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.CHUNKS WHERE DOC_ID IN ({lst})"
        ).collect()
        # Then delete from documents
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS WHERE DOC_ID IN ({lst})"
        ).collect()
        return len(ids)
    except Exception as e:
        print(f"Document delete error: {e}")
        return 0


# ==========================================
# FINANCIAL QUERY DETECTION
# ==========================================
def is_financial_query(query):
    """Detect if query is financial in nature"""
    if not query:
        return False

    query_lower = query.lower()
    financial_keywords = FINANCIAL_RAG_CONFIG["financial_keywords"]

    # Count financial keyword matches
    keyword_matches = sum(1 for kw in financial_keywords if kw in query_lower)

    # Check for numbers/metrics
    has_numbers = bool(
        re.search(r"\d+(\.\d+)?\s*(million|billion|m|b|%|percent)?", query_lower)
    )

    # Check for financial questions
    is_question = any(
        phrase in query_lower
        for phrase in [
            "how much",
            "in quarter",
            "revenue",
            "profit",
            "loss",
            "income",
            "tax rate",
        ]
    )

    # Query is financial if it has multiple keywords or numbers + financial terms
    return (
        (keyword_matches >= 2) or (has_numbers and keyword_matches >= 1) or is_question
    )


# ==========================================
# CHAT FUNCTIONS
# ==========================================
def new_chat(user, title="New Chat"):
    if not user:
        return None
    sid = str(uuid.uuid4())
    try:
        session.sql(
            f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.CHAT_SESSIONS (SESSION_ID, USERNAME, TITLE) VALUES ('{sid}', '{esc(user.upper())}', '{esc(title)}')"
        ).collect()
        return sid
    except Exception as e:
        print(f"New chat error: {e}")
        return None


def save_msg(sid, role, content, sources=None):
    if not sid or not role:
        return False
    mid = str(uuid.uuid4())
    src = ",".join(sources) if sources else ""
    content_safe = content if content else ""
    try:
        session.sql(
            f"INSERT INTO {DB_NAME}.{SCHEMA_NAME}.CHAT_MESSAGES (MESSAGE_ID, SESSION_ID, ROLE, CONTENT, SOURCES) VALUES ('{mid}', '{esc(sid)}', '{esc(role)}', '{esc(content_safe)}', '{esc(src)}')"
        ).collect()
        session.sql(
            f"UPDATE {DB_NAME}.{SCHEMA_NAME}.CHAT_SESSIONS SET UPDATED_AT=CURRENT_TIMESTAMP() WHERE SESSION_ID='{esc(sid)}'"
        ).collect()
        return True
    except Exception as e:
        print(f"Save message error: {e}")
        return False


def get_chats(user, pg=0, sz=15):
    if not user:
        return pd.DataFrame(columns=["SESSION_ID", "TITLE", "UPDATED_AT"])
    sql = f"SELECT SESSION_ID, TITLE, UPDATED_AT FROM {DB_NAME}.{SCHEMA_NAME}.CHAT_SESSIONS WHERE UPPER(USERNAME)='{esc(user.upper())}' ORDER BY UPDATED_AT DESC"
    return df_page(sql, pg, sz)


def get_msgs(sid):
    if not sid:
        return pd.DataFrame(columns=["ROLE", "CONTENT"])
    try:
        return session.sql(
            f"SELECT ROLE, CONTENT FROM {DB_NAME}.{SCHEMA_NAME}.CHAT_MESSAGES WHERE SESSION_ID='{esc(sid)}' ORDER BY CREATED_AT"
        ).to_pandas()
    except:
        return pd.DataFrame(columns=["ROLE", "CONTENT"])


def del_chat(sid):
    if not sid:
        return False
    try:
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.CHAT_MESSAGES WHERE SESSION_ID='{esc(sid)}'"
        ).collect()
        session.sql(
            f"DELETE FROM {DB_NAME}.{SCHEMA_NAME}.CHAT_SESSIONS WHERE SESSION_ID='{esc(sid)}'"
        ).collect()
        return True
    except Exception as e:
        print(f"Delete chat error: {e}")
        return False


def load_chat(sid):
    if not sid:
        return
    st.session_state.sid = sid
    df = get_msgs(sid)
    if df is not None and not df.empty:
        st.session_state.msgs = [
            {"role": r["ROLE"], "content": r["CONTENT"]} for _, r in df.iterrows()
        ]
    else:
        st.session_state.msgs = []


# ==========================================
# MARKDOWN TO HTML CONVERTER (ENHANCED)
# ==========================================
def md_to_html(text):
    """Convert markdown to clean, well-formatted HTML"""
    if not text:
        return ""

    text = str(text)

    # Code blocks first (before other processing)
    def replace_code_block(match):
        code = match.group(1).strip()
        code = code.replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre><code>{code}</code></pre>"

    text = re.sub(r"```(?:\w+)?\n?(.*?)```", replace_code_block, text, flags=re.DOTALL)

    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Headers with better spacing
    text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # Lists with proper structure
    lines = text.split("\n")
    result = []
    in_list = False
    list_type = None

    for line in lines:
        stripped = line.strip()

        # Handle unordered lists
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list or list_type != "ul":
                if in_list:
                    result.append(f"</{list_type}>")
                result.append("<ul>")
                in_list = True
                list_type = "ul"
            result.append(f"<li>{stripped[2:]}</li>")

        # Handle ordered lists
        elif re.match(r"^\d+\. ", stripped):
            if not in_list or list_type != "ol":
                if in_list:
                    result.append(f"</{list_type}>")
                result.append("<ol>")
                in_list = True
                list_type = "ol"

            cleaned_text = re.sub(r"^\d+\. ", "", stripped)
            result.append(f"<li>{cleaned_text}</li>")

        else:
            if in_list:
                result.append(f"</{list_type}>")
                in_list = False
                list_type = None
            result.append(line)

    if in_list:
        result.append(f"</{list_type}>")

    text = "\n".join(result)

    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    # Paragraphs - only wrap non-block elements
    def wrap_paragraphs(match):
        content = match.group(1)
        # Don't wrap if it's already a block element
        if content.strip().startswith(("<h", "<ul", "<ol", "<pre", "<div", "<table")):
            return content
        return f"<p>{content}</p>"

    # Split by double newlines and wrap in paragraphs
    paragraphs = re.split(r"\n\s*\n", text)
    new_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if para.startswith(("<h", "<ul", "<ol", "<pre", "<div", "<table")):
            new_paragraphs.append(para)
        else:
            # Replace single newlines with <br> within paragraphs
            para = para.replace("\n", "<br>")
            new_paragraphs.append(f"<p>{para}</p>")

    text = "\n\n".join(new_paragraphs)

    return text


# ==========================================
# ENHANCED RAG SEARCH
# ==========================================
def search(query, team, admin, mode="quick"):
    """Enhanced search with financial logic and fallback"""
    if not query or not str(query).strip():
        return "Please enter a valid question.", []

    query = str(query).strip()

    try:
        # Detect if this is a financial query
        is_financial = is_financial_query(query)
        config = FINANCIAL_RAG_CONFIG if is_financial else RAG_CONFIG

        model = MODEL_LARGE if (mode == "deep" or is_financial) else MODEL_SMALL

        if is_financial:
            st.info("🔍 Detected financial query - using enhanced financial search")

        cat_filter = ""
        if not admin:
            cats = get_categories(team)
            if not cats:
                return "🔒 No document access. Contact administrator.", []
            cat_list = "', '".join([str(c) for c in cats if c])
            if cat_list:
                cat_filter = f"AND UPPER(d.CATEGORY) IN ('{cat_list}')"

        escaped_query = esc(query)

        # First search attempt
        search_sql = build_search_sql(escaped_query, cat_filter, config, is_financial)

        try:
            df = session.sql(search_sql).to_pandas()
        except Exception as sql_err:
            return f"Database search error: {sql_err}", []

        # Fallback search if no results and financial query
        if (df is None or df.empty) and is_financial:
            st.warning("🔍 No results found, trying fallback search...")
            df = fallback_search(escaped_query, cat_filter, config)

        if df is None or df.empty:
            return "No relevant information found in your documents.", []

        # Process results with number extraction for financial queries
        context_parts, sources = process_search_results(df, config, is_financial)

        if not context_parts:
            return "No relevant information found in documents.", []

        context = "\n\n---\n\n".join(context_parts)

        # Enhanced prompts
        prompt = build_enhanced_prompt(query, context, mode, is_financial)

        try:
            max_prompt_len = 28000
            if len(prompt) > max_prompt_len:
                prompt = prompt[:max_prompt_len] + "..."

            answer_sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{esc(prompt)}')"
            result = qry(answer_sql, None)

            if not result or not isinstance(result, list) or len(result) == 0:
                return "Error: No response from AI model.", sources

            first_row = result[0]
            if first_row is None:
                return "Error: Null response from AI model.", sources

            answer = None
            try:
                if hasattr(first_row, "__getitem__"):
                    answer = first_row[0]
                elif hasattr(first_row, "asDict"):
                    row_dict = first_row.asDict()
                    if row_dict:
                        answer = list(row_dict.values())[0]
            except:
                pass

            if answer is None:
                return "Error: Could not extract AI response.", sources

            return str(answer), sources

        except Exception as e:
            return f"Error: {str(e)}", []

    except Exception as e:
        return f"Search error: {str(e)}", ""


def build_search_sql(query, cat_filter, config, is_financial=False):
    """Build enhanced search SQL with financial boosting"""

    number_boost = ""
    boost_select = ""
    if is_financial:
        numbers = re.findall(r"\d+(?:\.\d+)?", query)
        if numbers:
            number_conditions = " OR ".join(
                [
                    f"REGEXP_LIKE(LOWER(CHUNK_TEXT), '\\b{num}\\b')"
                    for num in numbers[:3]
                ]
            )
            number_boost = f"""
                , number_boost AS (
                    SELECT
                        CHUNK_TEXT,
                        FILENAME,
                        CATEGORY,
                        DOC_ID,
                        score,
                        START_LINE,
                        END_LINE,
                        CASE WHEN ({number_conditions})
                             THEN {config.get('number_boost_factor', 1.5)}
                             ELSE 1.0 END AS boost_factor
                    FROM candidates
                )
            """
            # use the boosted score in the window
            boost_select = "score * boost_factor"
        else:
            boost_select = "score"
    else:
        boost_select = "score"

    # source for the window function
    from_source = "number_boost" if is_financial and number_boost else "candidates"

    search_sql = f"""
        WITH
        qvec AS (
            SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('{EMBED_MODEL}', '{query}') AS v
        ),
        candidates AS (
            SELECT
                c.CHUNK_TEXT,
                d.FILENAME,
                d.CATEGORY,
                d.DOC_ID,
                VECTOR_COSINE_SIMILARITY(c.CHUNK_VEC, q.v) AS score,
                REGEXP_SUBSTR(c.CHUNK_TEXT, '=== LINES (\\d+)-(\\d+) ===', 1, 1, 'e', 1) AS START_LINE,
                REGEXP_SUBSTR(c.CHUNK_TEXT, '=== LINES (\\d+)-(\\d+) ===', 1, 1, 'e', 2) AS END_LINE
            FROM {DB_NAME}.{SCHEMA_NAME}.CHUNKS c
            JOIN {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS d
              ON c.DOC_ID = d.DOC_ID
            CROSS JOIN qvec q
            WHERE 1=1 {cat_filter}
            ORDER BY score DESC
            LIMIT {config['rerank_candidates']}
        )
        {number_boost if is_financial and number_boost else ''}
        , ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY DOC_ID ORDER BY {boost_select} DESC) AS rn
            FROM {from_source}
            WHERE score >= {config['similarity_threshold']}
        )
        SELECT
            CHUNK_TEXT,
            FILENAME,
            CATEGORY,
            score,
            START_LINE,
            END_LINE
        FROM ranked
        WHERE rn = 1
        ORDER BY score DESC
        LIMIT {config['max_chunks']}
    """

    return search_sql


def fallback_search(query, cat_filter, config):
    """Fallback search with relaxed parameters for financial queries"""
    fallback_sql = f"""
        WITH
        qvec AS (
            SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('{EMBED_MODEL}', '{query}') as v
        ),
        candidates AS (
            SELECT
                c.CHUNK_TEXT,
                d.FILENAME,
                d.CATEGORY,
                d.DOC_ID,
                VECTOR_COSINE_SIMILARITY(c.CHUNK_VEC, q.v) as score
            FROM {DB_NAME}.{SCHEMA_NAME}.CHUNKS c
            JOIN {DB_NAME}.{SCHEMA_NAME}.DOCUMENTS d ON c.DOC_ID = d.DOC_ID
            CROSS JOIN qvec q
            WHERE 1=1 {cat_filter}
            ORDER BY score DESC
            LIMIT 100  # Broader search
        )
        SELECT 
            CHUNK_TEXT, 
            FILENAME, 
            CATEGORY,
            score
        FROM candidates
        WHERE score >= 0.08  # Lower threshold
        ORDER BY score DESC
        LIMIT {config['max_chunks']}
    """

    try:
        return session.sql(fallback_sql).to_pandas()
    except:
        return None


def process_search_results(df, config, is_financial):
    """Process search results and extract sources"""
    context_parts = []
    sources = []

    for _, row in df.iterrows():
        try:
            chunk_text = str(row["CHUNK_TEXT"]) if "CHUNK_TEXT" in row else ""
            filename = str(row["FILENAME"]) if "FILENAME" in row else "Unknown"
            category = str(row["CATEGORY"]) if "CATEGORY" in row else "Unknown"

            # Remove line number metadata for context but keep it for reference
            clean_chunk = re.sub(r"=== LINES \d+-\d+ ===\n", "", chunk_text)
            clean_chunk = re.sub(r"\[L\d{4}\] ", "", clean_chunk)

            # Truncate if needed
            safe_text = (
                clean_chunk[: config["max_chunk_text"]]
                if len(clean_chunk) > config["max_chunk_text"]
                else clean_chunk
            )

            # Add line references for financial queries
            if is_financial and "start_line" in row:
                line_ref = f" (Lines {row['start_line']}-{row['end_line']})"
            else:
                line_ref = ""

            context_parts.append(
                f"**{filename}** (Category: {category}){line_ref}\n{safe_text}"
            )

            if filename not in sources:
                sources.append(filename)
        except Exception as e:
            print(f"Row processing error: {e}")
            continue

    return context_parts, sources


def build_enhanced_prompt(query, context, mode, is_financial):
    """Build enhanced prompt with financial accuracy focus"""

    if is_financial:
        # Financial-specific prompt
        if mode == "deep":
            prompt = f"""[INST]You are an expert financial analyst. Accuracy with numbers is CRITICAL.
CONTEXT:
{context}
QUESTION: {query}
INSTRUCTIONS:
1. FIRST, extract and verify ALL numbers, dates, and financial metrics
2. Cross-reference numbers across sources for consistency
3. Provide a structured Analysis of the financial data
4. Then, provide a precise Final Answer with exact figures
5. Cite specific line numbers when available
6. If numbers differ between sources, note the discrepancy
7. NEVER approximate financial figures - use exact numbers from context

Format:
## Analysis
(Step-by-step financial reasoning with numbers)
## Answer
(Precise final answer with exact figures)
[/INST]"""
        else:
            prompt = f"""[INST]You are a precise financial assistant. NUMERICAL ACCURACY IS MANDATORY.
CONTEXT:
{context}
QUESTION: {query}
INSTRUCTIONS:
- ANSWER DIRECTLY with exact numbers from context
- If multiple sources show different numbers, report all with sources
- Cite document and line numbers for financial figures
- DO NOT approximate or round unless explicitly stated
- If context lacks the exact figure, state "Exact figure not found"
- BE CONCISE but COMPLETE with all relevant numbers
[/INST]"""
    else:
        # Original prompts
        if mode == "deep":
            prompt = f"""[INST]You are an expert research assistant. Analyze the provided context carefully.
CONTEXT:
{context}
QUESTION: {query}
INSTRUCTIONS:
1. First, provide a structured Analysis of the relevant information.
2. Then, provide a comprehensive Final Answer.
Format your response using these headers:
## Analysis
(Your step-by-step reasoning)
## Answer
(Your final answer)
[/INST]"""
        else:
            prompt = f"""[INST]You are a precise knowledge assistant.
CONTEXT:
{context}
QUESTION: {query}
INSTRUCTIONS:
- Answer directly based on the context.
- If information is missing, say so.
- Be concise but complete.
- Cite sources when possible.
[/INST]"""

    return prompt


# ==========================================
# SESSION STATE
# ==========================================
if "sid" not in st.session_state:
    st.session_state.sid = None
if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "view" not in st.session_state:
    st.session_state.view = "chat"
if "pg" not in st.session_state:
    st.session_state.pg = {}
if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "quick"
# Selection states for bulk operations
if "selected_items" not in st.session_state:
    st.session_state.selected_items = {
        "users": set(),
        "teams": set(),
        "rules": set(),
        "docs": set(),
    }
# Admin edit states
if "edit_team" not in st.session_state:
    st.session_state.edit_team = None
if "edit_cat_access" not in st.session_state:
    st.session_state.edit_cat_access = None

# ==========================================
# USER CONTEXT
# ==========================================
curr_user = get_current_user()
curr_admin = check_is_admin(curr_user)
curr_team = "SUPER_ADMIN" if curr_admin else get_team(curr_user)
curr_access = get_access(curr_team, curr_admin)


# ==========================================
# UI RENDERING HELPERS (ENHANCED FOR ADMIN)
# ==========================================
def render_bulk_action_bar(item_type, items, delete_func, assign_func=None):
    """Render a unified bulk action bar"""
    selected = st.session_state.selected_items[item_type]

    if not selected:
        return

    with st.container():
        st.markdown('<div class="bulk-action-bar">', unsafe_allow_html=True)
        cols = st.columns([2, 1, 1, 1])

        cols[0].markdown(f"**📌 {len(selected)} item(s) selected**")

        if assign_func and item_type == "users":
            teams = get_teams()
            target_team = cols[1].selectbox(
                "Assign to", teams, key=f"bulk_assign_{item_type}"
            )
            if cols[2].button("✓ Assign", use_container_width=True):
                assign_func(list(selected), target_team)
                st.success(f"✅ Assigned {len(selected)} users to {target_team}")
                st.session_state.selected_items[item_type].clear()
                st.rerun()

        # Delete button with confirmation
        confirm_key = f"confirm_delete_{item_type}"
        if cols[3].button("🗑️ Delete", use_container_width=True, type="primary"):
            if st.checkbox(
                f"⚠️ Confirm delete {len(selected)} item(s)?", key=confirm_key
            ):
                count = delete_func(list(selected))
                st.success(f"✅ Deleted {count} item(s)")
                st.session_state.selected_items[item_type].clear()
                st.rerun()

        if cols[0].button("Clear Selection", key=f"clear_{item_type}"):
            st.session_state.selected_items[item_type].clear()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def render_select_all(item_type, df, id_column):
    """Render select all checkbox"""
    col1, col2, col3, col4 = st.columns([1, 4, 3, 3])

    if col1.checkbox("Select All", key=f"select_all_{item_type}"):
        ids = df[id_column].tolist() if df is not None and not df.empty else []
        st.session_state.selected_items[item_type] = set(ids)


def render_item_row(item_type, item_id, content_items, is_selected):
    """Render a single item row with checkbox"""
    row_class = "item-row selected" if is_selected else "item-row"
    st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)

    cols = st.columns([1, 8])  # Checkbox + content

    # Checkbox
    if cols[0].checkbox("", key=f"sel_{item_type}_{item_id}", value=is_selected):
        st.session_state.selected_items[item_type].add(item_id)
    else:
        st.session_state.selected_items[item_type].discard(item_id)

    # Content
    with cols[1]:
        col_count = len(content_items)
        content_cols = st.columns(col_count)
        for i, content in enumerate(content_items):
            content_cols[i].write(content)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# UI INTEGRATION
# ==========================================
# In the User Management view, add password reset per user:


# Add this to the user row rendering in the 'users' view:
def render_user_row_with_password_reset(username, team, is_admin):
    """Enhanced user row with password reset button"""
    is_selected = username in st.session_state.selected_items["users"]

    st.markdown(
        f'<div class="item-row {"selected" if is_selected else ""}">',
        unsafe_allow_html=True,
    )
    cols = st.columns([0.5, 4, 3, 2, 1.5, 1.5])

    # Checkbox
    if cols[0].checkbox("", key=f"sel_users_{username}", value=is_selected):
        st.session_state.selected_items["users"].add(username)
    else:
        st.session_state.selected_items["users"].discard(username)

    # User info
    cols[1].write(f"`{username}`")
    cols[2].write(team)
    cols[3].write(admin)

    # Password reset button
    if cols[4].button("🔑 Reset", key=f"reset_pwd_{username}"):
        st.session_state[f"reset_modal_{username}"] = True

    # Delete button
    if cols[5].button("🗑️", key=f"del_user_{username}"):
        count = bulk_delete([username])
        if count > 0:
            st.success("✅ User deleted")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Password reset modal
    if st.session_state.get(f"reset_modal_{username}", False):
        with st.expander(f"🔑 Reset Password for {username}", expanded=True):
            with st.form(f"reset_form_{username}"):
                new_pwd = st.text_input(
                    "New Password", type="password", key=f"new_pwd_{username}"
                )
                confirm_pwd = st.text_input(
                    "Confirm Password", type="password", key=f"confirm_pwd_{username}"
                )
                col_a, col_b = st.columns(2)
                if col_a.form_submit_button("Reset", type="primary"):
                    if new_pwd == confirm_pwd and len(new_pwd) >= 6:
                        ok, msg = reset_user_password(username, new_pwd)
                        if ok:
                            st.success(f"✅ {msg}")
                            del st.session_state[f"reset_modal_{username}"]
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("❌ Passwords don't match or too short")
                if col_b.form_submit_button("Cancel"):
                    del st.session_state[f"reset_modal_{username}"]
                    st.rerun()


# ==========================================
# SIDEBAR (ENHANCED WITH ADMIN DASHBOARD SUMMARY)
# ==========================================
with st.sidebar:
    st.markdown(
        """
    <div class="logo-box">
        <div class="logo-icon">🏢</div>
        <div class="logo-name">AIFAQ Pro</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if curr_admin:
        st.markdown(
            '<span class="badge badge-admin">Admin</span>', unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<span class="badge badge-user">{curr_team}</span>', unsafe_allow_html=True
        )

    st.caption(f"User: `{curr_user}`")
    st.divider()

    if st.button("✨ New Chat", use_container_width=True, type="primary"):
        st.session_state.sid = None
        st.session_state.msgs = []
        st.session_state.view = "chat"
        st.rerun()

    st.markdown('<div class="section-title">Recent Chats</div>', unsafe_allow_html=True)
    chats = get_chats(curr_user, st.session_state.pg.get("chats", 0), 8)

    if chats is not None and not chats.empty:
        for _, r in chats.iterrows():
            c1, c2 = st.columns([5, 1])
            title_raw = r.get("TITLE", "Chat") if hasattr(r, "get") else r["TITLE"]
            title_str = str(title_raw) if title_raw else "Chat"
            title = title_str[:18] + "..." if len(title_str) > 18 else title_str
            session_id = str(
                r.get("SESSION_ID", "") if hasattr(r, "get") else r["SESSION_ID"]
            )

            with c1:
                if st.button(
                    f"💬 {title}", key=f"c_{session_id[:8]}", use_container_width=True
                ):
                    load_chat(session_id)
                    st.session_state.view = "chat"
                    st.rerun()
            with c2:
                if st.button("×", key=f"d_{session_id[:8]}"):
                    del_chat(session_id)
                    if st.session_state.sid == session_id:
                        st.session_state.sid = None
                        st.session_state.msgs = []
                    st.rerun()
    else:
        st.caption("No conversations yet")

    if curr_admin:
        st.divider()
        st.markdown(
            '<div class="section-title">Admin Dashboard</div>', unsafe_allow_html=True
        )
        # Quick stats
        col1, col2 = st.columns(2)
        col1.metric("Users", count_tbl("APP_USER_TEAMS"))
        col2.metric("Documents", count_tbl("DOCUMENTS"))
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👥 Users", use_container_width=True):
                st.session_state.view = "users"
                st.session_state.selected_items = {
                    k: set() for k in st.session_state.selected_items
                }  # Clear selections
                st.rerun()
            if st.button("🔐 Access", use_container_width=True):
                st.session_state.view = "access"
                st.session_state.selected_items = {
                    k: set() for k in st.session_state.selected_items
                }
                st.rerun()
        with col2:
            if st.button("🏷️ Teams", use_container_width=True):
                st.session_state.view = "teams"
                st.session_state.selected_items = {
                    k: set() for k in st.session_state.selected_items
                }
                st.rerun()
            if st.button("📂 Docs", use_container_width=True):
                st.session_state.view = "docs"
                st.session_state.selected_items = {
                    k: set() for k in st.session_state.selected_items
                }
                st.rerun()

# ==========================================
# MAIN CONTENT
# =========================================#
if curr_team == "GUEST" and not curr_admin:
    st.warning("🔒 You are not assigned to a team. Please contact an administrator.")
    st.stop()

view = st.session_state.view

# ==========================================
# CHAT VIEW (IMPROVED RENDERING)
# =========================================#
if view == "chat":
    # Messages Container
    if st.session_state.msgs:
        for m in st.session_state.msgs:
            role = m.get("role", "")
            content = m.get("content", "")

            if role == "user":
                safe_content = str(content).replace("<", "&lt;").replace(">", "&gt;")
                st.markdown(
                    f'<div class="message-container"><div class="user-msg">{safe_content}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                # Parse AI response
                answer_content = str(content)
                sources = []
                thinking_html = ""

                # Extract sources
                if "📚 **Sources:**" in answer_content:
                    parts = answer_content.split("📚 **Sources:**")
                    answer_content = parts[0].strip()
                    if len(parts) > 1:
                        sources = [s.strip() for s in parts[1].split(",") if s.strip()]

                # Extract thinking section
                if "## Analysis" in answer_content and "## Answer" in answer_content:
                    parts = answer_content.split("## Answer")
                    thinking = parts[0].replace("## Analysis", "").strip()
                    answer_content = parts[1].strip() if len(parts) > 1 else ""

                    thinking_html = f"""
                    <div class="thinking-box">
                        <div class="thinking-label">🧠 Analysis</div>
                        <div class="ai-msg-content">{md_to_html(thinking)}</div>
                    </div>
                    """

                # Convert main answer to HTML
                answer_html = md_to_html(answer_content)

                # Build final AI message
                ai_message_html = f'<div class="message-container"><div class="ai-msg">'

                if thinking_html:
                    ai_message_html += thinking_html

                ai_message_html += f'<div class="ai-msg-content">{answer_html}</div>'

                # Add sources
                if sources:
                    source_tags = "".join(
                        [f'<span class="source-tag">📄 {s}</span>' for s in sources]
                    )
                    ai_message_html += f"""
                    <div class="sources-box">
                        <div class="sources-label">📚 Sources</div>
                        {source_tags}
                    </div>
                    """

                ai_message_html += "</div></div>"

                st.markdown(ai_message_html, unsafe_allow_html=True)

    # Mode Selector
    mode_cols = st.columns([1, 1, 3])
    with mode_cols[0]:
        if st.button(
            "⚡ Quick" if st.session_state.ai_mode != "quick" else "⚡ Quick ✓",
            use_container_width=True,
            type="primary" if st.session_state.ai_mode == "quick" else "secondary",
        ):
            st.session_state.ai_mode = "quick"
            st.rerun()
    with mode_cols[1]:
        if st.button(
            "🧠 Deep" if st.session_state.ai_mode != "deep" else "🧠 Deep ✓",
            use_container_width=True,
            type="primary" if st.session_state.ai_mode == "deep" else "secondary",
        ):
            st.session_state.ai_mode = "deep"
            st.rerun()
    with mode_cols[2]:
        model_name = MODEL_LARGE if st.session_state.ai_mode == "deep" else MODEL_SMALL
        st.caption(f"Model: **{model_name}**")

    # Chat Input
    query = st.chat_input("Ask a question about your documents...")

    # Process query
    if query:
        if not st.session_state.sid:
            title = query[:45] + "..." if len(query) > 45 else query
            st.session_state.sid = new_chat(curr_user, title)

        st.session_state.msgs.append({"role": "user", "content": query})
        save_msg(st.session_state.sid, "user", query)

        with st.spinner("🔍 Searching documents..."):
            answer, sources = search(
                query, curr_team, curr_admin, mode=st.session_state.ai_mode
            )
            if sources:
                answer += f"\n\n📚 **Sources:** {', '.join(sources)}"

        st.session_state.msgs.append({"role": "assistant", "content": answer})
        save_msg(st.session_state.sid, "assistant", answer, sources)
        st.rerun()

# ==========================================
# ADMIN VIEWS WITH ENHANCED UI
# =========================================#
elif view == "users" and curr_admin:
    st.markdown(
        '<div class="page-title">👥 User Management</div>', unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 2], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">➕ Create User</h3></div>',
            unsafe_allow_html=True,
        )
        with st.form("create_user_form", clear_on_submit=True):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            teams = get_teams()
            new_team = st.selectbox("Assign Team", ["None"] + teams)
            submitted = st.form_submit_button("Create User", type="primary")
            if submitted:
                if not new_username or not new_password:
                    st.error("❌ Username and password required.")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match.")
                else:
                    ok, msg = create_user(
                        new_username,
                        new_password,
                        new_team if new_team != "None" else None,
                    )
                    if ok:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">📋 All Users</h3></div>',
            unsafe_allow_html=True,
        )

        df = load_users()
        if df is not None and not df.empty:
            # Deduplicate users to prevent key conflicts
            df = df.drop_duplicates(subset=["USERNAME"], keep="first")

            # Bulk Action Bar (for assign & delete)
            render_bulk_action_bar("users", df, bulk_delete, bulk_assign)

            # Table Header
            h1, h2, h3, h4, h5, h6 = st.columns([0.5, 4, 3, 2, 1.5, 1.5])
            h2.write("**Username**")
            h3.write("**Team**")
            h4.write("**Admin**")
            h5.write("")
            h6.write("")

            # User Rows with Password Reset
            for idx, (_, row) in enumerate(df.iterrows()):
                username = row["USERNAME"].strip()  # Clean whitespace
                team = row["TEAM"]
                admin = row["ADMIN"]
                render_user_row_with_password_reset(username, team, admin)
        else:
            st.info("No users found.")

        st.markdown("</div>", unsafe_allow_html=True)

elif view == "teams" and curr_admin:
    st.markdown(
        '<div class="page-title">🏷️ Team Management</div>', unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 2], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">➕ Create Team</h3></div>',
            unsafe_allow_html=True,
        )
        with st.form("create_team_form", clear_on_submit=True):
            new_team_name = st.text_input("Team Name")
            new_desc = st.text_input("Description (optional)")
            submitted = st.form_submit_button("Create Team", type="primary")
            if submitted and new_team_name:
                ok, msg = create_team_db(new_team_name, new_desc)
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">📋 Existing Teams</h3></div>',
            unsafe_allow_html=True,
        )
        teams = get_teams()
        if teams:
            for team in teams:
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.write(f"**{team}**")
                with col2:
                    if st.button("✏️", key=f"edit_team_{team}"):
                        st.session_state.edit_team = team
                with col3:
                    if st.button("🗑️", key=f"del_team_{team}"):
                        ok, msg = delete_team_db(team)
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            # Edit team modal
            if st.session_state.edit_team:
                edit_team = st.session_state.edit_team
                with st.expander(f"✏️ Editing: {edit_team}", expanded=True):
                    with st.form("edit_team_form"):
                        new_name = st.text_input("New Team Name", value=edit_team)
                        new_desc = st.text_input(
                            "New Description",
                            value=val(
                                f"SELECT DESCRIPTION FROM {DB_NAME}.{SCHEMA_NAME}.TEAMS WHERE TEAM_NAME='{esc(edit_team)}'"
                            ),
                        )
                        col_a, col_b = st.columns(2)
                        if col_a.form_submit_button("Save Changes", type="primary"):
                            # Simple update: delete old, create new if name changes
                            if new_name != edit_team:
                                delete_team_db(edit_team)
                                create_team_db(new_name, new_desc)
                            else:
                                session.sql(
                                    f"UPDATE {DB_NAME}.{SCHEMA_NAME}.TEAMS SET DESCRIPTION='{esc(new_desc)}' WHERE TEAM_NAME='{esc(edit_team)}'"
                                ).collect()
                            st.success("✅ Team updated")
                            st.session_state.edit_team = None
                            st.rerun()
                        if col_b.form_submit_button("Cancel"):
                            st.session_state.edit_team = None
                            st.rerun()
        else:
            st.info("No teams yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">🔍 Team Details</h3></div>',
            unsafe_allow_html=True,
        )
        selected_team = st.selectbox("Select Team", get_teams())
        if selected_team:
            members = load_members(selected_team)
            if members is not None and not members.empty:
                st.dataframe(members, hide_index=True, use_container_width=True)
            else:
                st.info("No members in this team.")
        st.markdown("</div>", unsafe_allow_html=True)

elif view == "access" and curr_admin:
    st.markdown(
        '<div class="page-title">🔐 Access Control</div>', unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 2], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">➕ Grant Team Access</h3></div>',
            unsafe_allow_html=True,
        )
        teams = get_teams()
        all_cats = get_all_categories()
        with st.form("grant_access_form", clear_on_submit=True):
            grant_team = st.selectbox("Team", teams if teams else ["No teams"])
            grant_cats = st.multiselect("Categories", all_cats)
            submitted = st.form_submit_button("Grant", type="primary")
            if submitted and grant_team and grant_cats:
                n = bulk_grant(grant_team, grant_cats)
                st.success(f"✅ Granted {n} categories")

        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">👑 Manage Admins</h3></div>',
            unsafe_allow_html=True,
        )
        admins = load_admins()
        if admins is not None and not admins.empty:
            # Deduplicate admins to prevent key conflicts
            admins = admins.drop_duplicates(subset=["USERNAME"], keep="first")

            # Info about system grants
            st.caption("ℹ️ Admins granted by 'SYSTEM' cannot be removed")

            # Use enumerate to ensure unique keys
            for idx, (_, row) in enumerate(admins.iterrows()):
                col1, col2 = st.columns([4, 1])
                username = row["USERNAME"].strip()  # Clean any trailing spaces
                granted_by = row["GRANTED_BY"]

                # Check if this is a system-granted admin
                is_system_grant = granted_by and str(granted_by).upper().startswith(
                    "SYSTEM"
                )

                with col1:
                    st.write(f"`{username}` (Granted by: {granted_by})")

                with col2:
                    if is_system_grant:
                        st.button(
                            "🚫",
                            key=f"revoke_admin_{username}_{idx}",
                            disabled=True,
                            help="Cannot remove system-granted admins",
                        )
                    else:
                        if st.button(
                            "🗑️",
                            key=f"revoke_admin_{username}_{idx}",
                            help=f"Revoke admin from {username}",
                        ):
                            ok, msg = remove_admin_db(username, curr_user)
                            if ok:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
        else:
            st.info("No admins yet.")

        with st.expander("➕ Grant Admin Access"):
            with st.form("grant_admin_form", clear_on_submit=True):
                grant_user = st.text_input("Username to Grant Admin")
                submitted = st.form_submit_button("Grant Admin", type="primary")
                if submitted and grant_user:
                    ok, msg = add_admin_db(grant_user, curr_user)
                    if ok:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        # Category Management (Centralized)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">🏷️ Manage Categories</h3></div>',
            unsafe_allow_html=True,
        )
        with st.expander("➕ Add New Category", expanded=False):
            with st.form("add_cat_access", clear_on_submit=True):
                new_cat = st.text_input("Category Name")
                if st.form_submit_button("Create"):
                    if new_cat:
                        ok, msg = create_category_db(new_cat)
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

        categories = get_all_categories()
        if categories:
            for cat in categories:
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.write(f"**{cat}**")
                with col2:
                    if st.button("✏️", key=f"edit_cat_access_{cat}"):
                        st.session_state.edit_cat_access = cat
                with col3:
                    if st.button("🗑️", key=f"del_cat_access_{cat}"):
                        ok, msg = delete_category_db(cat)
                        if ok:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            if st.session_state.edit_cat_access:
                edit_cat = st.session_state.edit_cat_access
                with st.expander(f"✏️ Editing: {edit_cat}", expanded=True):
                    with st.form("edit_cat_access_form"):
                        new_name = st.text_input("New Name", value=edit_cat)
                        col_a, col_b = st.columns(2)
                        if col_a.form_submit_button("Save", type="primary"):
                            if new_name != edit_cat:
                                delete_category_db(edit_cat)
                                create_category_db(new_name)
                            st.success("✅ Category updated")
                            st.session_state.edit_cat_access = None
                            st.rerun()
                        if col_b.form_submit_button("Cancel"):
                            st.session_state.edit_cat_access = None
                            st.rerun()
        else:
            st.info("No categories yet.")

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">📋 Access Rules</h3></div>',
            unsafe_allow_html=True,
        )

        df = load_rules()
        if df is not None and not df.empty:
            render_bulk_action_bar(
                "rules",
                df,
                lambda rules: bulk_revoke(
                    [
                        (r["TEAM"], r["CATEGORY"])
                        for _, r in df.iterrows()
                        if (r["TEAM"], r["CATEGORY"]) in rules
                    ]
                ),
            )

            render_select_all("rules", df, None)  # No single ID, use composite

            h1, h2, h3, h4 = st.columns([0.5, 4, 4, 1])
            h2.write("**Team**")
            h3.write("**Category**")
            h4.write("")

            # Deduplicate rules to prevent key conflicts
            df = df.drop_duplicates(subset=["TEAM", "CATEGORY"], keep="first")

            for idx, (_, row) in enumerate(df.iterrows()):
                team = row["TEAM"]
                cat = row["CATEGORY"]
                rule_id = (team, cat)
                is_selected = rule_id in st.session_state.selected_items["rules"]
                render_item_row("rules", rule_id, [team, cat], is_selected)

                if not is_selected:
                    dcol = st.columns([0.5, 4, 4, 1])[3]
                    # Add idx to ensure unique key
                    if dcol.button("🗑️", key=f"revoke_rule_{team}_{cat}_{idx}"):
                        ok, msg = revoke_cat(team, cat)
                        if ok:
                            st.success("✅ Revoked")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
        else:
            st.info("No rules yet.")

        st.markdown("</div>", unsafe_allow_html=True)

elif view == "docs" and curr_admin:
    st.markdown(
        '<div class="page-title">📂 Document Management</div>', unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 2], gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">📤 Upload Document</h3></div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])
        all_cats = get_all_categories()

        if all_cats:
            selected_cat = st.selectbox("Assign to Category", all_cats)
        else:
            st.warning("No categories yet. Manage in Access Control.")
            selected_cat = None

        if uploaded_file and selected_cat:
            if st.button("Index Document", use_container_width=True, type="primary"):
                with st.spinner("Indexing document..."):
                    ok, msg = ingest_doc(uploaded_file, selected_cat)
                    if ok:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
        elif uploaded_file and not selected_cat:
            st.info("Please create or select a category first.")

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="admin-card-header"><h3 class="admin-icon">📑 Uploaded Documents</h3></div>',
            unsafe_allow_html=True,
        )

        df = load_docs()
        if df is not None and not df.empty:
            df["UPLOAD_TS"] = pd.to_datetime(df["UPLOAD_TS"]).dt.strftime(
                "%Y-%m-%d %H:%M"
            )

            # Bulk Action Bar
            render_bulk_action_bar("docs", df, delete_docs)

            # Select All Row
            render_select_all("docs", df, "DOC_ID")

            # Table Header
            h1, h2, h3, h4, h5, h6 = st.columns([0.5, 4, 2.5, 2.5, 2, 1])
            h2.write("**Filename**")
            h3.write("**Category**")
            h4.write("**Uploaded By**")
            h5.write("**Date**")
            h6.write("")

            # Document Rows
            for _, row in df.iterrows():
                doc_id = row["DOC_ID"]
                is_selected = doc_id in st.session_state.selected_items["docs"]

                render_item_row(
                    "docs",
                    doc_id,
                    [
                        row["FILENAME"],
                        f"`{row['CATEGORY']}`",
                        row["UPLOADED_BY"],
                        row["UPLOAD_TS"],
                    ],
                    is_selected,
                )

                # Individual delete button in last column
                if not is_selected:  # Avoid double controls
                    dcol = st.columns([0.5, 4, 2.5, 2.5, 2, 1])[5]
                    if dcol.button("🗑️", key=f"del_doc_{doc_id}"):
                        count = delete_docs([doc_id])
                        if count > 0:
                            st.success("✅ Document deleted")
                            st.rerun()
        else:
            st.info("No documents uploaded yet.")

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.session_state.view = "chat"
    st.rerun()

# AIFAQ Pro version 2 - Complete Deployment & User Guide

This README provides comprehensive instructions for deploying AIFAQ Pro to Snowflake Marketplace and using it effectively.

---

## 📂 File Structure Overview

Your deployment package contains 5 essential files:

```
aifaq-pro-app/version_2/
├── app_version2.py       # Main Streamlit application (our provided code)
├── manifest.yml          # App configuration & metadata
├── setup.sql             # Database objects & schema setup
├── environment.yml       # Python environment & dependencies
└── snowflake.yml         # SnowCLI deployment configuration
```

---

## 🚀 Deployment Methods

### **Method 1: SnowCLI (Recommended for Developers)**

#### Step 1: Install SnowCLI
```bash
# Install via pip
pip install snowflake-cli-labs

# Verify installation
snow --version
```

#### Step 2: Configure Connection
```bash
# Interactive setup
snow connection add

# Or create config manually at ~/.snowflake/config.toml
[connections.marketplace_deploy]
account = "your-account"
user = "your_username"
warehouse = "COMPUTE_WH"
role = "ACCOUNTADMIN"
authenticator = "snowflake"
```

#### Step 3: Deploy Application
```bash
# Navigate to project folder
cd version_2

# Deploy (creates package and app)
snow app run

# Check status
snow app list
```

#### Step 4: Create Marketplace Package
```bash
# Add a version
snow app version create 1.0.0

# Upload to stage
snow app version upload 1.0.0

# Create release directive for marketplace
snow app version get-release-directive 1.0.0
```

---

### **Method 2: Snowflake UI (Classic Console)**

#### Step 1: Create Application Package
```sql
-- Run as ACCOUNTADMIN
CREATE APPLICATION PACKAGE AIFAQ_PRO_PKG 
    DISTRIBUTION = PUBLIC 
    COMMENT = 'AI-powered FAQ assistant for enterprises';
```

#### Step 2: Upload Files to Stage

In Snowsight or Classic UI:
1. Navigate to **Data > Databases > AIFAQ_PRO_PKG > Stages**
2. Click on the automatically created stage
3. Upload all 7 files using the **+ Files** button

Or use SQL:
```sql
-- Stage each file
PUT file:///path/to/aifaq_app.py @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/manifest.yml @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/setup.sql @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/environment.yml @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/snowflake.yml @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/requirements.txt @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
PUT file:///path/to/LICENSE @AIFAQ_PRO_PKG.stage/1.0.0/ OVERWRITE=TRUE;
```

#### Step 3: Add Version to Package
```sql
-- Create version from staged files
ALTER APPLICATION PACKAGE AIFAQ_PRO_PKG 
    ADD VERSION 1.0.0 
    USING '@AIFAQ_PRO_PKG.stage/1.0.0';
```

#### Step 4: Create Test Application (Optional)
```sql
-- Test before publishing
CREATE APPLICATION AIFAQ_PRO_TEST 
    FROM APPLICATION PACKAGE AIFAQ_PRO_PKG 
    USING VERSION 1.0.0;
```

---

### **Method 3: Snowflake UI (Snowsight)**

#### Step 1: Enable Partner Connect
1. Go to **Admin > Partner Connect**
2. Enable **Snowflake Native Apps Development**

#### Step 2: Create Package
1. Navigate to **Data Products > Native Apps**
2. Click **Create Application Package**
3. Fill in:
   - Name: `AIFAQ_PRO_PKG`
   - Distribution: `Public`
   - Comment: Description

#### Step 3: Upload & Release
1. In your package, go to **Versions**
2. Click **Create Version**
3. Drag-and-drop all 7 files
4. Set version number to `1.0.0`
5. Click **Create Release Directive**

---

## 🎯 Post-Installation Setup

After deploying, complete these **mandatory** steps:

### **1. Grant Cortex Privileges**
```sql
-- Run as ACCOUNTADMIN in consumer account
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO APPLICATION AIFAQ_PRO_APP;

-- Grant warehouse access
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO APPLICATION AIFAQ_PRO_APP;
```

### **2. Verify Installation**
```sql
-- Check if app is running
SHOW APPLICATIONS;

-- Should see: AIFAQ_PRO_APP | RUNNING
```

### **3. Launch Streamlit App**
1. Go to **Data Products > Native Apps**
2. Click on **AIFAQ Pro**
3. Click **Open Streamlit App**

---

## 👤 User Guide

### **For First-Time Admin Users**

#### Step 1: Initial Login
- The user who installed the app is automatically the first admin
- **Username**: Your Snowflake username
- **Password**: Your Snowflake password (single sign-on via Streamlit)

#### Step 2: Create Teams
1. In sidebar, click **🏷️ Teams**
2. Click **➕ Create Team**
3. Enter team name (e.g., "Finance", "Engineering")
4. Click **Create Team**

#### Step 3: Create Categories
1. Go to **🔐 Access Control**
2. Expand **🏷️ Manage Categories**
3. Click **➕ Add New Category**
4. Enter category name (e.g., "Financial Docs", "HR Policies")
5. Click **Create**

#### Step 4: Grant Access
1. Still in **Access Control**
2. Under **➕ Grant Team Access**:
   - Select Team (e.g., "Finance")
   - Select Categories (e.g., "Financial Docs", "General")
   - Click **Grant**

#### Step 5: Add Users
1. Go to **👥 User Management**
2. Under **➕ Create User**:
   - Username: `JOHN_DOE`
   - Password: Min 6 characters
   - Team: Select from dropdown
   - Click **Create User**
3. Repeat for all users

#### Step 6: Upload Documents
1. Go to **📂 Document Management**
2. Under **📤 Upload Document**:
   - Choose file (PDF, TXT, DOCX)
   - Select Category
   - Click **Index Document**
3. Wait for confirmation: *"Document indexed with X chunks"*

---

### **For End Users (Non-Admin)**

#### Step 1: Login
- Your admin will provide credentials
- **Note**: First-time users in "GUEST" team have no access until assigned

#### Step 2: Start Chatting
1. Click **✨ New Chat** in sidebar
2. Type question in chat input
3. Toggle mode:
   - **⚡ Quick**: Fast answers
   - **🧠 Deep**: Detailed analysis
4. View sources below each answer

#### Step 3: View History
- All previous chats appear in sidebar
- Click any chat to resume
- Use **×** to delete old chats

---

## 🔧 Configuration & Customization

### **Modifying RAG Settings**
Edit these values in `aifaq_app.py` under **ENHANCED CONSTANTS & CONFIGS**:

```python
RAG_CONFIG = {
    "max_chunks": 6,              # Reduce for faster responses
    "similarity_threshold": 0.15,  # Increase for stricter matching
    "rerank_candidates": 25,      # Increase for better recall
    "max_chunk_text": 700,        # Reduce for faster embedding
}
```

### **Changing AI Models**
In `aifaq_app.py`, update:

```python
MODEL_SMALL = "mistral-7b"      # For Quick mode
MODEL_LARGE = "mixtral-8x7b"    # For Deep mode
EMBED_MODEL = "snowflake-arctic-embed-m"  # Keep this fixed
```

**Supported Models by Region**: Check [Snowflake Cortex Docs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)

### **Adding New File Types**
In `setup.sql`, modify stage:
```sql
CREATE STAGE DOC_STAGE
    FILE_FORMAT = (TYPE = 'CSV')  -- Supports BINARY for any file type
```

---

## 🐛 Troubleshooting

### **App Won't Start**
**Error**: `"Failed to start application"`
- **Solution**: Grant Cortex privileges (see Post-Installation Setup #1)
- **Solution**: Check warehouse exists and is running

### **"No document access" Error**
**Cause**: User not assigned to team or team lacks category access
- **Solution**: 
  1. Admin: Go to User Management
  2. Assign user to a team
  3. In Access Control, grant team → category mapping

### **Document Upload Fails**
**Error**: `"Failed to parse document"`
- **Solution**: Verify file type (PDF, TXT, DOCX only)
- **Solution**: Check file size (< 50MB recommended)
- **Solution**: Grant stage WRITE privileges:
```sql
GRANT WRITE ON STAGE AIFAQ_PRO_APP.APP_SCHEMA.DOC_STAGE TO APPLICATION ROLE AIFAQ_PRO_APP.PUBLIC;
```

### **Slow Chat Responses**
- **Solution**: Use **⚡ Quick Mode** instead of 🧠 Deep
- **Solution**: Reduce `RAG_CONFIG["max_chunks"]` to 3-4
- **Solution**: Upgrade warehouse size (Medium → Large)
- **Solution**: Check for unoptimized queries in `search()` function

### **Embedding Errors**
**Error**: `"SQL compilation error: cortex function not available"`
- **Solution**: Confirm `snowflake-arctic-embed-m` is available in your region
- **Solution**: Run: `GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO APPLICATION AIFAQ_PRO_APP;`

### **User Creation Fails**
**Error**: `"Invalid username or password < 6 chars"`
- **Solution**: Username must be alphanumeric + underscores only
- **Solution**: Password must be ≥ 6 characters
- **Solution**: User must not already exist in Snowflake account

---

## 📊 Monitoring & Maintenance

### **View App Usage**
```sql
-- Run as ACCOUNTADMIN
SELECT * FROM TABLE(AIFAQ_PRO_APP.APP_SCHEMA.CHAT_SESSIONS());
SELECT COUNT(*) FROM AIFAQ_PRO_APP.APP_SCHEMA.DOCUMENTS;
```

### **Clean Up Old Data**
```sql
-- Delete chats older than 30 days
DELETE FROM AIFAQ_PRO_APP.APP_SCHEMA.CHAT_SESSIONS 
WHERE CREATED_AT < DATEADD(DAY, -30, CURRENT_TIMESTAMP());

-- Delete orphaned chunks
DELETE FROM AIFAQ_PRO_APP.APP_SCHEMA.CHUNKS 
WHERE DOC_ID NOT IN (SELECT DOC_ID FROM AIFAQ_PRO_APP.APP_SCHEMA.DOCUMENTS);
```

### **Backup Configuration**
Export important tables:
```sql
COPY INTO @my_backup_stage/
FROM AIFAQ_PRO_APP.APP_SCHEMA.TEAMS
FILE_FORMAT = (TYPE = CSV);
```

---

## 🏪 Publishing to Snowflake Marketplace

### **Step 1: Prepare Listing**

1. **Screenshots**: Capture 3-5 key screens (Chat, Admin Dashboard, Document Upload)
2. **Icon**: Create 200x200px PNG icon (the 🏢 emoji works as placeholder)
3. **Description**: Write compelling app description (max 2000 chars)
4. **Pricing**: Decide:
   - **Free**: No charges
   - **Paid**: Set monthly/annual price
   - **BYOL**: Customers bring their own license

### **Step 2: Submit via Provider Portal**

1. Go to [Snowflake Marketplace Provider Portal](https://providers.snowflake.com)
2. Click **Create Listing**
3. Fill in:
   - **Listing Name**: AIFAQ Pro
   - **Category**: AI/ML
   - **Package**: `AIFAQ_PRO_PKG`
   - **Version**: `1.0.0`
   - **Regions**: Select all available regions
4. Upload:
   - README.md
   - Screenshots
   - Icon
   - Support contact
5. Submit for Review

### **Step 3: Certification Process**
- Snowflake reviews security, performance, and compliance
- Typical timeline: 5-10 business days
- Address any feedback promptly

### **Step 4: Go Live**
- Once approved, click **Publish**
- App becomes visible in Snowflake Marketplace
- Monitor analytics in Provider Portal

---

## 📞 Support & Resources

### **Documentation**
- [Snowflake Native Apps Docs](https://docs.snowflake.com/en/developer-guide/native-apps/overview)
- [Cortex LLM Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)

### **Community**
- [Snowflake Community](https://community.snowflake.com)
- [Stack Overflow: snowflake-native-apps](https://stackoverflow.com/questions/tagged/snowflake-native-apps)

### **Contact**
- **Technical Issues**: Open issue in your repository
- **Feature Requests**: Use GitHub Issues with `enhancement` label
- **Emergency Support**: Email info@aifaq.pro ( might take 1 to 2 days for reply)

---

## 🔄 Updating the App

### **Minor Updates (Bug Fixes)**

```bash
# Update code
# Bump version in manifest.yml (e.g., 1.0.0 → 1.0.1)
snow app version create 1.0.1
snow app version upload 1.0.1
```

In UI:
```sql
ALTER APPLICATION PACKAGE AIFAQ_PRO_PKG 
    ADD VERSION 1.0.1 USING '@AIFAQ_PRO_PKG.stage/1.0.1';
```

### **Major Updates (New Features)**

1. Update version in:
   - `manifest.yml` (version)
   - `snowflake.yml` (version)
2. Add to `setup.sql`:
```sql
-- Migration script for v2.0
ALTER TABLE APP_USER_TEAMS ADD COLUMN IF NOT EXISTS EMAIL VARCHAR;
```
3. Deploy new version
4. Test thoroughly before releasing
5. Update marketplace listing

---

## 📋 Pre-Deployment Checklist

Before deploying to production, verify:

- [ ] All 5 files are present and validated
- [ ] `manifest.yml` has correct author/contact info
- [ ] `setup.sql` has no syntax errors (test in worksheet)
- [ ] `environment.yml` uses supported Python version (3.10)
- [ ] Cortex models are available in target regions
- [ ] Default warehouse exists (`COMPUTE_WH`)
- [ ] Created at least 3 test users and 2 teams
- [ ] Uploaded sample documents in each category
- [ ] Tested both Quick and Deep modes
- [ ] Verified admin functions (grant/revoke access)
- [ ] Added company branding (logo, colors)
- [ ] Created demo video (2-3 minutes)
- [ ] Set up support email/portal
- [ ] Prepared pricing strategy
- [ ] Added telemetry for usage analytics

---

##  Quick Start Summary

**For Admins**:
1. Deploy → Grant Cortex → Launch App
2. Create Teams → Create Categories → Grant Access
3. Add Users → Upload Documents → Done!

**For Users**:
1. Login → New Chat → Ask Questions → View Sources

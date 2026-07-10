import urllib.parse
from sqlalchemy import create_engine, text

# Using our new application user credentials
password = urllib.parse.quote_plus("crm_pass123") 
DATABASE_URL = f"mysql+pymysql://crm_user:{password}@localhost:3306/hcp_crm"

print("Testing connection with dedicated application user...")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Connected successfully to MySQL:", result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)
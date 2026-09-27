"""
DURGAM DB Diagnostic Script
Checks if durgam_sovereign.db exists, lists tables, and row counts.
"""
import os, sys, sqlite3, json

# DB_PATH matches db_service.py logic:
# os.path.dirname(os.path.dirname(os.path.dirname(__file__))) where __file__ is services/db_service.py
# So from backend/: one level up is project root
project_root = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(project_root, "backend", "durgam_sovereign.db")

print(f"Project Root : {project_root}")
print(f"DB Path      : {db_path}")
print(f"DB Exists    : {os.path.exists(db_path)}")

if not os.path.exists(db_path):
    print("\n[ERROR] Database file NOT found.")
    print("Run: uvicorn app.main:app --host 0.0.0.0 --port 8000  (in backend/ dir)")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cursor.fetchall()]
print(f"\nTables found: {tables}\n")

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
    count = cursor.fetchone()[0]
    print(f"  {table:35s} => {count:5d} rows")

if "incidents" in tables:
    print("\n--- Latest 3 Incidents ---")
    cursor.execute("SELECT case_id, ack_number, victim_name, status FROM incidents ORDER BY rowid DESC LIMIT 3")
    rows = cursor.fetchall()
    for r in rows:
        print(f"  CaseID={r[0]}, Ack={r[1]}, Victim={r[2]}, Status={r[3]}")
    if not rows:
        print("  No rows yet.")

if "api_keys" in tables:
    print("\n--- API Keys ---")
    cursor.execute("SELECT key_id, owner_name, role, is_active FROM api_keys LIMIT 5")
    for r in cursor.fetchall():
        print(f"  KeyID={r[0]}, Owner={r[1]}, Role={r[2]}, Active={r[3]}")

conn.close()
print("\n[OK] Database check complete.")

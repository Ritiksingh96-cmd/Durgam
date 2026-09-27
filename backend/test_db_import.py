import sys, os
sys.path.insert(0, '.')

from app.services.db_service import DB_PATH, get_all_incidents

print("DB_PATH:", DB_PATH)
print("Exists:", os.path.exists(DB_PATH))

cases = get_all_incidents(5)
print(f"Incidents fetched from DB: {len(cases)}")
for c in cases:
    print(f"  {c['case_id']} | {c.get('victim_name','?')} | {c.get('status','?')}")

print("\n[OK] DB import works correctly!")

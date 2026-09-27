import sqlite3, os

db_path = r'R:\All Working Projects Ls\Durgam\backend\durgam_sovereign.db'
print('DB Size:', os.path.getsize(db_path), 'bytes')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cursor.fetchall()]
print('Tables:', tables)

for t in tables:
    cursor.execute(f'SELECT COUNT(*) FROM [{t}]')
    count = cursor.fetchone()[0]
    print(f'  {t}: {count} rows')

if 'incidents' in tables:
    print('\n--- Last 5 Incidents ---')
    cursor.execute('SELECT case_id, ack_number, victim_name, status FROM incidents ORDER BY rowid DESC LIMIT 5')
    for r in cursor.fetchall():
        print(f'  {r[0]} | {r[1]} | {r[2]} | {r[3]}')

if 'api_keys' in tables:
    print('\n--- API Keys ---')
    cursor.execute('SELECT key_id, owner_name, role, is_active FROM api_keys LIMIT 10')
    for r in cursor.fetchall():
        print(f'  {r[0]} | {r[1]} | {r[2]} | active={r[3]}')

if 'audit_logs' in tables:
    print('\n--- Last 3 Audit Logs ---')
    cursor.execute('SELECT log_id, actor, action, target_id FROM audit_logs ORDER BY rowid DESC LIMIT 3')
    for r in cursor.fetchall():
        print(f'  {r[0]} | {r[1]} | {r[2]} | {r[3]}')

conn.close()
print('\n[OK] Done')
